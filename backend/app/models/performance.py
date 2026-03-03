from app import db
from datetime import datetime

class Performance(db.Model):
    """Student performance records"""
    __tablename__ = 'performances'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    # Academic Performance
    semester = db.Column(db.Integer, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    internal_marks = db.Column(db.Float, default=0.0)
    external_marks = db.Column(db.Float, default=0.0)
    total_marks = db.Column(db.Float, default=0.0)
    grade = db.Column(db.String(5))
    credits = db.Column(db.Integer, default=3)
    
    # Attendance & Participation
    attendance_percentage = db.Column(db.Float, default=0.0)
    assignment_score = db.Column(db.Float, default=0.0)
    lab_performance = db.Column(db.Float, default=0.0)
    
    # Study Metrics
    study_hours_per_week = db.Column(db.Float, default=0.0)
    participation_score = db.Column(db.Float, default=0.0)
    
    # Discipline
    discipline_score = db.Column(db.Float, default=100.0)
    
    # Metadata
    academic_year = db.Column(db.String(20))
    month = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'semester': self.semester,
            'subject_name': self.subject_name,
            'internal_marks': self.internal_marks,
            'external_marks': self.external_marks,
            'total_marks': self.total_marks,
            'grade': self.grade,
            'credits': self.credits,
            'attendance_percentage': self.attendance_percentage,
            'assignment_score': self.assignment_score,
            'lab_performance': self.lab_performance,
            'study_hours_per_week': self.study_hours_per_week,
            'participation_score': self.participation_score,
            'discipline_score': self.discipline_score,
            'academic_year': self.academic_year,
            'month': self.month,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Performance {self.student_id} - {self.subject_name}>'


class ChatHistory(db.Model):
    """Chat history with AI mentor"""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    context = db.Column(db.Text)  # JSON string with student context
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'message': self.message,
            'response': self.response,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ChatHistory {self.student_id} - {self.created_at}>'


class Prediction(db.Model):
    """Prediction records"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    prediction_type = db.Column(db.String(50), nullable=False)  # gpa, scholarship, career, risk
    input_data = db.Column(db.Text)  # JSON string
    output_data = db.Column(db.Text)  # JSON string
    confidence_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'prediction_type': self.prediction_type,
            'input_data': self.input_data,
            'output_data': self.output_data,
            'confidence_score': self.confidence_score,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Prediction {self.prediction_type} - {self.student_id}>'


class Alert(db.Model):
    """Alerts and notifications"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # risk, attendance, performance
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    email_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read,
            'email_sent': self.email_sent,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Alert {self.alert_type} - {self.student_id}>'
