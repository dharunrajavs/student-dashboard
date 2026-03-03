from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.student import Student
from app.models.performance import Performance, Prediction
from app.services.gpa_predictor import gpa_predictor_service
from app.services.scholarship_predictor import scholarship_predictor_service
from app.services.career_recommender import career_recommendation_service
from app.services.risk_scorer import risk_scoring_service
import json

bp = Blueprint('predictions', __name__)

@bp.route('/gpa', methods=['POST'])
@jwt_required()
def predict_gpa():
    """
    Predict semester GPA
    ---
    tags:
      - Predictions
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            student_id:
              type: integer
            internal_marks:
              type: number
            attendance_percentage:
              type: number
            assignment_score:
              type: number
            lab_performance:
              type: number
            previous_gpa:
              type: number
            study_hours_per_week:
              type: number
            participation_score:
              type: number
    responses:
      200:
        description: GPA prediction result
    """
    try:
        data = request.get_json()
        
        # Predict GPA
        result = gpa_predictor_service.predict(data)
        
        # Save prediction to database
        if data.get('student_id'):
            prediction = Prediction(
                student_id=data['student_id'],
                prediction_type='gpa',
                input_data=json.dumps(data),
                output_data=json.dumps(result),
                confidence_score=result.get('confidence_score')
            )
            db.session.add(prediction)
            db.session.commit()
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/scholarship', methods=['POST'])
@jwt_required()
def predict_scholarship():
    """
    Predict scholarship eligibility
    ---
    tags:
      - Predictions
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            student_id:
              type: integer
            gpa:
              type: number
            attendance_percentage:
              type: number
            family_income:
              type: number
            extracurricular_score:
              type: number
            discipline_score:
              type: number
            research_publications:
              type: integer
    responses:
      200:
        description: Scholarship eligibility result
    """
    try:
        data = request.get_json()
        
        # Predict scholarship eligibility
        result = scholarship_predictor_service.predict(data)
        
        # Save prediction
        if data.get('student_id'):
            prediction = Prediction(
                student_id=data['student_id'],
                prediction_type='scholarship',
                input_data=json.dumps(data),
                output_data=json.dumps(result),
                confidence_score=result.get('probability')
            )
            db.session.add(prediction)
            db.session.commit()
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/career', methods=['POST'])
@jwt_required()
def recommend_career():
    """
    Get career recommendations
    ---
    tags:
      - Predictions
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            student_id:
              type: integer
            gpa:
              type: number
            subject_scores:
              type: object
            interests:
              type: array
              items:
                type: string
            skills:
              type: array
              items:
                type: string
            coding_ability:
              type: string
    responses:
      200:
        description: Career recommendations
    """
    try:
        data = request.get_json()
        
        # Get recommendations
        recommendations = career_recommendation_service.recommend(data)
        
        # Save prediction
        if data.get('student_id'):
            prediction = Prediction(
                student_id=data['student_id'],
                prediction_type='career',
                input_data=json.dumps(data),
                output_data=json.dumps(recommendations),
                confidence_score=recommendations[0]['match_score'] if recommendations else 0
            )
            db.session.add(prediction)
            db.session.commit()
        
        return jsonify({
            'recommendations': recommendations,
            'total': len(recommendations)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/risk-score/<int:student_id>', methods=['GET'])
@jwt_required()
def calculate_risk_score(student_id):
    """
    Calculate student risk score
    ---
    tags:
      - Predictions
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
    responses:
      200:
        description: Risk score calculation
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Calculate risk score
        result = risk_scoring_service.calculate_risk_score(student_id)
        
        # Save prediction
        prediction = Prediction(
            student_id=student_id,
            prediction_type='risk',
            input_data=json.dumps({'student_id': student_id}),
            output_data=json.dumps(result),
            confidence_score=100 - result.get('risk_score', 50)
        )
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/history/<int:student_id>', methods=['GET'])
@jwt_required()
def get_prediction_history(student_id):
    """
    Get prediction history for a student
    ---
    tags:
      - Predictions
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
      - in: query
        name: type
        type: string
    responses:
      200:
        description: Prediction history
    """
    try:
        query = Prediction.query.filter_by(student_id=student_id)
        
        # Filter by type if provided
        prediction_type = request.args.get('type')
        if prediction_type:
            query = query.filter_by(prediction_type=prediction_type)
        
        predictions = query.order_by(Prediction.created_at.desc()).limit(20).all()
        
        return jsonify({
            'predictions': [p.to_dict() for p in predictions],
            'total': len(predictions)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
