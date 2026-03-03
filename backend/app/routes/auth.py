from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db, limiter
from app.models.user import User
from app.models.student import Student
from flasgger import swag_from

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - username
            - password
            - role
          properties:
            email:
              type: string
            username:
              type: string
            password:
              type: string
            role:
              type: string
              enum: [student, faculty, admin]
            student_data:
              type: object
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid input
      409:
        description: User already exists
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 409
        
        # Create user
        user = User(
            email=data['email'],
            username=data['username'],
            role=data.get('role', 'student')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()
        
        # Create student profile if role is student
        if user.role == 'student' and data.get('student_data'):
            student_data = data['student_data']
            student = Student(
                user_id=user.id,
                roll_number=student_data.get('roll_number'),
                first_name=student_data.get('first_name'),
                last_name=student_data.get('last_name'),
                department=student_data.get('department'),
                semester=student_data.get('semester', 1),
                batch=student_data.get('batch'),
                phone=student_data.get('phone'),
                gender=student_data.get('gender'),
                coding_ability=student_data.get('coding_ability', 'intermediate'),
                interests=student_data.get('interests'),
                skills=student_data.get('skills'),
                family_income=student_data.get('family_income')
            )
            db.session.add(student)
        
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """
    User login
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json()
        
        user = User.query.filter_by(username=data.get('username')).first()
        
        if not user or not user.check_password(data.get('password')):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        response_data = {
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }
        
        # Add student info if user is a student
        if user.role == 'student' and user.student:
            response_data['student'] = user.student.to_dict()
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Token refreshed successfully
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=str(identity))
    return jsonify({'access_token': access_token}), 200


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user profile
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: User profile
      404:
        description: User not found
    """
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        response_data = {'user': user.to_dict()}
        
        if user.role == 'student' and user.student:
            response_data['student'] = user.student.to_dict(include_performance=True)
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change user password
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - old_password
            - new_password
          properties:
            old_password:
              type: string
            new_password:
              type: string
    responses:
      200:
        description: Password changed successfully
      400:
        description: Invalid old password
    """
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        data = request.get_json()
        
        if not user.check_password(data.get('old_password')):
            return jsonify({'error': 'Invalid old password'}), 400
        
        user.set_password(data.get('new_password'))
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
