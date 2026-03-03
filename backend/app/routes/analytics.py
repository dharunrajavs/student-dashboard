from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.student import Student
from app.models.performance import Performance
from sqlalchemy import func, extract
from datetime import datetime, timedelta

bp = Blueprint('analytics', __name__)

@bp.route('/heatmap/<int:student_id>', methods=['GET'])
@jwt_required()
def get_performance_heatmap(student_id):
    """
    Get performance heatmap data
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
    responses:
      200:
        description: Heatmap data
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        performances = Performance.query.filter_by(
            student_id=student_id
        ).order_by(Performance.created_at.desc()).all()
        
        # Subject vs Performance heatmap
        subject_performance = {}
        for perf in performances:
            subject = perf.subject_name
            if subject not in subject_performance:
                subject_performance[subject] = []
            
            subject_performance[subject].append({
                'marks': perf.total_marks,
                'attendance': perf.attendance_percentage,
                'month': perf.month or perf.created_at.month
            })
        
        # Calculate averages and risk levels
        heatmap_data = []
        for subject, records in subject_performance.items():
            avg_marks = sum(r['marks'] for r in records) / len(records)
            avg_attendance = sum(r['attendance'] for r in records) / len(records)
            
            # Determine color (risk level)
            if avg_marks >= 75 and avg_attendance >= 85:
                color = 'green'
                risk_level = 'Good'
            elif avg_marks >= 60 and avg_attendance >= 75:
                color = 'yellow'
                risk_level = 'Moderate'
            else:
                color = 'red'
                risk_level = 'Risk'
            
            heatmap_data.append({
                'subject': subject,
                'average_marks': round(avg_marks, 2),
                'average_attendance': round(avg_attendance, 2),
                'records_count': len(records),
                'color': color,
                'risk_level': risk_level
            })
        
        # Monthly performance trend
        monthly_trend = {}
        for perf in performances:
            month = perf.month or perf.created_at.month
            if month not in monthly_trend:
                monthly_trend[month] = []
            
            monthly_trend[month].append(perf.total_marks)
        
        trend_data = [
            {
                'month': month,
                'average_marks': round(sum(marks) / len(marks), 2),
                'records_count': len(marks)
            }
            for month, marks in sorted(monthly_trend.items())
        ]
        
        return jsonify({
            'student_id': student_id,
            'subject_performance': heatmap_data,
            'monthly_trend': trend_data,
            'total_subjects': len(subject_performance)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/trends/<int:student_id>', methods=['GET'])
@jwt_required()
def get_performance_trends(student_id):
    """
    Get performance trends and analytics
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
    responses:
      200:
        description: Performance trends
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        performances = Performance.query.filter_by(
            student_id=student_id
        ).order_by(Performance.created_at.asc()).all()
        
        if not performances:
            return jsonify({'error': 'No performance data available'}), 404
        
        # Calculate trends
        marks_trend = [p.total_marks for p in performances]
        attendance_trend = [p.attendance_percentage for p in performances]
        
        # Calculate improvement/decline
        if len(marks_trend) >= 2:
            marks_change = marks_trend[-1] - marks_trend[0]
            attendance_change = attendance_trend[-1] - attendance_trend[0]
        else:
            marks_change = 0
            attendance_change = 0
        
        return jsonify({
            'student_id': student_id,
            'marks_trend': marks_trend,
            'attendance_trend': attendance_trend,
            'marks_change': round(marks_change, 2),
            'attendance_change': round(attendance_change, 2),
            'trend_direction': 'improving' if marks_change > 5 else 'declining' if marks_change < -5 else 'stable',
            'average_marks': round(sum(marks_trend) / len(marks_trend), 2),
            'average_attendance': round(sum(attendance_trend) / len(attendance_trend), 2),
            'total_records': len(performances)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    """
    Get student leaderboard
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - in: query
        name: department
        type: string
      - in: query
        name: semester
        type: integer
      - in: query
        name: limit
        type: integer
        default: 10
    responses:
      200:
        description: Student rankings
    """
    try:
        query = Student.query
        
        # Filter by department
        department = request.args.get('department')
        if department:
            query = query.filter_by(department=department)
        
        # Filter by semester
        semester = request.args.get('semester', type=int)
        if semester:
            query = query.filter_by(semester=semester)
        
        # Sort by CGPA
        students = query.order_by(Student.current_cgpa.desc()).limit(
            min(request.args.get('limit', 10, type=int), 50)
        ).all()
        
        leaderboard = []
        for rank, student in enumerate(students, 1):
            leaderboard.append({
                'rank': rank,
                'student_id': student.id,
                'roll_number': student.roll_number,
                'name': student.full_name,
                'department': student.department,
                'semester': student.semester,
                'cgpa': student.current_cgpa
            })
        
        return jsonify({
            'leaderboard': leaderboard,
            'total': len(leaderboard),
            'filters': {
                'department': department,
                'semester': semester
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/comparison/<int:student_id>', methods=['GET'])
@jwt_required()
def get_class_comparison(student_id):
    """
    Compare student performance with class average
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
    responses:
      200:
        description: Performance comparison
      404:
        description: Student not found
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Get class average (same department and semester)
        class_students = Student.query.filter_by(
            department=student.department,
            semester=student.semester
        ).all()
        
        if len(class_students) > 1:
            class_avg_cgpa = sum(s.current_cgpa for s in class_students) / len(class_students)
        else:
            class_avg_cgpa = student.current_cgpa
        
        # Get department average
        dept_students = Student.query.filter_by(department=student.department).all()
        dept_avg_cgpa = sum(s.current_cgpa for s in dept_students) / len(dept_students) if dept_students else 0
        
        # Calculate percentile
        students_below = Student.query.filter(
            Student.department == student.department,
            Student.semester == student.semester,
            Student.current_cgpa < student.current_cgpa
        ).count()
        
        percentile = (students_below / len(class_students)) * 100 if len(class_students) > 0 else 0
        
        return jsonify({
            'student_cgpa': student.current_cgpa,
            'class_average': round(class_avg_cgpa, 2),
            'department_average': round(dept_avg_cgpa, 2),
            'percentile': round(percentile, 2),
            'class_size': len(class_students),
            'performance_status': 'above_average' if student.current_cgpa > class_avg_cgpa else 'below_average'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
