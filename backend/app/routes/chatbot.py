from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.student import Student
from app.models.performance import ChatHistory
from app.services.chatbot import chatbot_service

bp = Blueprint('chatbot', __name__)

@bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    """
    Send message to AI chatbot mentor
    ---
    tags:
      - Chatbot
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - student_id
            - message
          properties:
            student_id:
              type: integer
            message:
              type: string
    responses:
      200:
        description: AI response
      400:
        description: Invalid input
      404:
        description: Student not found
    """
    try:
        data = request.get_json()
        
        if not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        student_id = data.get('student_id')
        message = data.get('message')
        
        # Verify student exists
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Get conversation history
        history = ChatHistory.query.filter_by(
            student_id=student_id
        ).order_by(ChatHistory.created_at.desc()).limit(5).all()
        
        history_data = [
            {'message': h.message, 'response': h.response}
            for h in reversed(history)
        ]
        
        # Generate AI response
        result = chatbot_service.generate_response(
            student_id=student_id,
            message=message,
            conversation_history=history_data
        )
        
        ai_response = result.get('response', 'I apologize, but I encountered an error. Please try again.')
        
        # Save to chat history
        chat_record = ChatHistory(
            student_id=student_id,
            message=message,
            response=ai_response,
            context=None
        )
        db.session.add(chat_record)
        db.session.commit()
        
        return jsonify({
            'message': message,
            'response': ai_response,
            'timestamp': chat_record.created_at.isoformat(),
            'success': result.get('success', False)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/history/<int:student_id>', methods=['GET'])
@jwt_required()
def get_chat_history(student_id):
    """
    Get chat history for a student
    ---
    tags:
      - Chatbot
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
      - in: query
        name: limit
        type: integer
        default: 50
    responses:
      200:
        description: Chat history
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        limit = min(request.args.get('limit', 50, type=int), 100)
        
        history = ChatHistory.query.filter_by(
            student_id=student_id
        ).order_by(ChatHistory.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'student_id': student_id,
            'history': [h.to_dict() for h in reversed(history)],
            'total': len(history)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/study-plan/<int:student_id>', methods=['GET'])
@jwt_required()
def get_study_plan(student_id):
    """
    Get personalized study plan
    ---
    tags:
      - Chatbot
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
    responses:
      200:
        description: Personalized study plan
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        study_plan = chatbot_service.generate_study_plan(student_id)
        
        if not study_plan:
            return jsonify({'error': 'Unable to generate study plan'}), 500
        
        return jsonify(study_plan), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/clear-history/<int:student_id>', methods=['DELETE'])
@jwt_required()
def clear_chat_history(student_id):
    """
    Clear chat history for a student
    ---
    tags:
      - Chatbot
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
    responses:
      200:
        description: History cleared
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        ChatHistory.query.filter_by(student_id=student_id).delete()
        db.session.commit()
        
        return jsonify({'message': 'Chat history cleared successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
