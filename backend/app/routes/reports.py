"""
Reports generation routes
"""
from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.student import Student
from app.models.performance import Performance, Prediction
from app.services.pdf_generator import pdf_generator
from app.services.email_service import email_service
from app.services.gpa_predictor import gpa_predictor_service
from app.services.risk_scorer import risk_scoring_service
from app.services.scholarship_predictor import scholarship_predictor_service
from datetime import datetime
import os

reports = Blueprint('reports', __name__, url_prefix='/api/reports')

@reports.route('/generate-pdf', methods=['POST'])
@jwt_required()
def generate_pdf_report():
    """Generate PDF report for student"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get student - either from user.student or from request
        student = user.student
        if not student:
            # If admin, try to get student_id from request
            data = request.get_json() or {}
            student_id = data.get('student_id')
            if student_id:
                student = Student.query.get(student_id)
            if not student:
                # Return a simple success response for non-student users
                return jsonify({
                    'message': 'PDF generation not available for admin users',
                    'success': False
                }), 200
        
        # Get student data
        student_data = {
            'first_name': student.first_name,
            'last_name': student.last_name,
            'roll_number': student.roll_number,
            'department': student.department,
            'semester': student.semester,
            'current_cgpa': student.current_cgpa or 0,
            'batch': student.batch
        }
        
        # Get performance data
        performances = Performance.query.filter_by(student_id=student.id).order_by(
            Performance.created_at.desc()
        ).all()
        
        performance_data = [{
            'subject_name': p.subject_name,
            'internal_marks': p.internal_marks,
            'external_marks': p.external_marks,
            'total_marks': p.total_marks,
            'grade': p.grade,
            'attendance_percentage': p.attendance_percentage
        } for p in performances]
        
        # Get or generate predictions
        predictions = {}
        
        # Get predictions by type
        for pred_type in ['gpa', 'scholarship', 'risk']:
            pred = Prediction.query.filter_by(student_id=student.id, prediction_type=pred_type).order_by(
                Prediction.created_at.desc()
            ).first()
            if pred and pred.output_data:
                import json
                try:
                    output_data = json.loads(pred.output_data) if isinstance(pred.output_data, str) else pred.output_data
                    if isinstance(output_data, dict):
                        key = 'gpa_prediction' if pred_type == 'gpa' else pred_type
                        predictions[key] = output_data
                except (json.JSONDecodeError, TypeError):
                    pass
        
        if not predictions:
            # Generate fresh predictions for report
            if performances:
                latest_perf = performances[0]
                
                # GPA prediction
                gpa_data = {
                    'internal_marks': latest_perf.internal_marks or 0,
                    'attendance_percentage': latest_perf.attendance_percentage or 0,
                    'assignment_score': latest_perf.assignment_score or 0,
                    'lab_performance': latest_perf.lab_performance or 0,
                    'previous_gpa': student.current_cgpa or 0,
                    'study_hours_per_week': latest_perf.study_hours_per_week or 0,
                    'participation_score': latest_perf.participation_score or 0
                }
                gpa_result = gpa_predictor_service.predict(gpa_data)
                predictions['gpa_prediction'] = gpa_result
                
                # Risk score
                risk_result = risk_scoring_service.calculate_risk_score(student.id)
                predictions['risk_score'] = risk_result
                
                # Scholarship
                scholar_data = {
                    'gpa': student.current_cgpa or 0,
                    'attendance': latest_perf.attendance_percentage or 0,
                    'family_income': student.family_income or 0,
                    'extracurricular_score': 75,
                    'discipline_score': latest_perf.discipline_score or 0,
                    'publications': 0
                }
                scholar_result = scholarship_predictor_service.predict(scholar_data)
                predictions['scholarship'] = scholar_result
        
        # Generate PDF
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        reports_dir = os.path.join(backend_dir, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{student.roll_number}_{timestamp}.pdf"
        output_path = os.path.join(reports_dir, filename)
        
        pdf_generator.generate_performance_report(
            student_data=student_data,
            performance_data=performance_data,
            predictions=predictions,
            output_path=output_path
        )
        
        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"academic_report_{student.roll_number}.pdf"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error generating PDF report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@reports.route('/email-report', methods=['POST'])
@jwt_required()
def email_report():
    """Generate and email PDF report to student"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        student = user.student
        if not student:
            # If admin, try to get student_id from request
            data = request.get_json() or {}
            student_id = data.get('student_id')
            if student_id:
                student = Student.query.get(student_id)
            if not student:
                return jsonify({
                    'message': 'Email report not available - no student profile linked',
                    'success': False
                }), 200
        
        # Generate report (same as above)
        student_data = {
            'first_name': student.first_name,
            'last_name': student.last_name,
            'roll_number': student.roll_number,
            'department': student.department,
            'semester': student.semester,
            'current_cgpa': student.current_cgpa or 0,
            'batch': student.batch
        }
        
        performances = Performance.query.filter_by(student_id=student.id).order_by(
            Performance.created_at.desc()
        ).all()
        
        performance_data = [{
            'subject_name': p.subject_name,
            'internal_marks': p.internal_marks,
            'external_marks': p.external_marks,
            'total_marks': p.total_marks,
            'grade': p.grade,
            'attendance_percentage': p.attendance_percentage
        } for p in performances]
        
        predictions = {}
        import json
        for pred_type in ['gpa', 'scholarship', 'risk']:
            pred = Prediction.query.filter_by(
                student_id=student.id, 
                prediction_type=pred_type
            ).order_by(Prediction.created_at.desc()).first()
            
            if pred and pred.output_data:
                try:
                    output_data = json.loads(pred.output_data) if isinstance(pred.output_data, str) else pred.output_data
                    key = 'gpa_prediction' if pred_type == 'gpa' else ('risk_score' if pred_type == 'risk' else pred_type)
                    predictions[key] = output_data
                except (json.JSONDecodeError, TypeError):
                    pass
        
        # Generate PDF
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        reports_dir = os.path.join(backend_dir, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{student.roll_number}_{timestamp}.pdf"
        output_path = os.path.join(reports_dir, filename)
        
        pdf_generator.generate_performance_report(
            student_data=student_data,
            performance_data=performance_data,
            predictions=predictions,
            output_path=output_path
        )
        
        # Send email
        student_name = f"{student.first_name} {student.last_name}"
        try:
            success = email_service.send_performance_report(
                user_email=user.email,
                student_name=student_name,
                report_file_path=output_path
            )
        except Exception as email_error:
            current_app.logger.warning(f"Email sending not configured: {str(email_error)}")
            # Return success but note email wasn't sent
            return jsonify({
                'message': 'Report generated successfully. Email sending is not configured.',
                'report_path': output_path,
                'success': True,
                'email_sent': False
            }), 200
        
        if success:
            return jsonify({
                'message': 'Report generated and sent successfully',
                'email': user.email
            }), 200
        else:
            # Return success but note email couldn't be sent (likely SMTP not configured)
            return jsonify({
                'message': 'Report generated but email sending failed. SMTP may not be configured.',
                'report_path': output_path,
                'success': True,
                'email_sent': False
            }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error emailing report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@reports.route('/send-alert', methods=['POST'])
@jwt_required()
def send_alert_notification():
    """Send alert notification email (admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        student_id = data.get('student_id')
        alert_title = data.get('title')
        alert_message = data.get('message')
        
        if not all([student_id, alert_title, alert_message]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        student = Student.query.get(student_id)
        if not student or not student.user:
            return jsonify({'error': 'Student not found'}), 404
        
        success = email_service.send_alert_email(
            user_email=student.user.email,
            alert_title=alert_title,
            alert_message=alert_message
        )
        
        if success:
            return jsonify({'message': 'Alert notification sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send alert'}), 500
        
    except Exception as e:
        current_app.logger.error(f"Error sending alert: {str(e)}")
        return jsonify({'error': str(e)}), 500
