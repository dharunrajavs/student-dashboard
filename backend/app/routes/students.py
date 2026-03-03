from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.student import Student
from app.models.performance import Performance

bp = Blueprint('students', __name__)

@bp.route('/profile/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_profile(student_id):
    """
    Get student profile
    ---
    tags:
      - Students
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
    responses:
      200:
        description: Student profile
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        return jsonify(student.to_dict(include_performance=True)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/profile/<int:student_id>', methods=['PUT'])
@jwt_required()
def update_student_profile(student_id):
    """
    Update student profile
    ---
    tags:
      - Students
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
    responses:
      200:
        description: Profile updated successfully
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = [
            'first_name', 'last_name', 'phone', 'department',
            'semester', 'interests', 'skills', 'coding_ability',
            'parent_name', 'parent_phone', 'parent_email'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(student, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'student': student.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/performance/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_performance(student_id):
    """
    Get student performance records
    ---
    tags:
      - Students
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
      - in: query
        name: semester
        type: integer
      - in: query
        name: subject
        type: string
    responses:
      200:
        description: Performance records
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        query = Performance.query.filter_by(student_id=student_id)
        
        # Filter by semester if provided
        semester = request.args.get('semester', type=int)
        if semester:
            query = query.filter_by(semester=semester)
        
        # Filter by subject if provided
        subject = request.args.get('subject')
        if subject:
            query = query.filter_by(subject_name=subject)
        
        performances = query.order_by(Performance.created_at.desc()).all()
        
        return jsonify({
            'student_id': student_id,
            'performances': [p.to_dict() for p in performances],
            'total_records': len(performances)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/performance', methods=['POST'])
@jwt_required()
def add_performance_record():
    """
    Add performance record
    ---
    tags:
      - Students
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
            - semester
            - subject_name
          properties:
            student_id:
              type: integer
            semester:
              type: integer
            subject_name:
              type: string
            internal_marks:
              type: number
            external_marks:
              type: number
            attendance_percentage:
              type: number
            assignment_score:
              type: number
            lab_performance:
              type: number
    responses:
      201:
        description: Performance record added
      400:
        description: Invalid input
    """
    try:
        data = request.get_json()
        
        performance = Performance(
            student_id=data['student_id'],
            semester=data['semester'],
            subject_name=data['subject_name'],
            internal_marks=data.get('internal_marks', 0),
            external_marks=data.get('external_marks', 0),
            attendance_percentage=data.get('attendance_percentage', 0),
            assignment_score=data.get('assignment_score', 0),
            lab_performance=data.get('lab_performance', 0),
            study_hours_per_week=data.get('study_hours_per_week', 0),
            participation_score=data.get('participation_score', 0),
            discipline_score=data.get('discipline_score', 100),
            academic_year=data.get('academic_year'),
            month=data.get('month')
        )
        
        # Calculate total marks
        performance.total_marks = performance.internal_marks + performance.external_marks
        
        db.session.add(performance)
        db.session.commit()
        
        return jsonify({
            'message': 'Performance record added successfully',
            'performance': performance.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/list', methods=['GET'])
@jwt_required()
def list_students():
    """
    List all students (admin/faculty only)
    ---
    tags:
      - Students
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
      - in: query
        name: department
        type: string
      - in: query
        name: semester
        type: integer
    responses:
      200:
        description: List of students
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        query = Student.query
        
        # Filter by department
        department = request.args.get('department')
        if department:
            query = query.filter_by(department=department)
        
        # Filter by semester
        semester = request.args.get('semester', type=int)
        if semester:
            query = query.filter_by(semester=semester)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'students': [s.to_dict() for s in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
