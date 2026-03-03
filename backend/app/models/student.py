from app import db
from datetime import datetime

class Student(db.Model):
    """Student model with academic information"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    
    # Academic Info
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    batch = db.Column(db.String(20))
    section = db.Column(db.String(10))
    current_cgpa = db.Column(db.Float, default=0.0)
    
    # Family Info
    family_income = db.Column(db.Float)
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))
    
    # Additional Info
    interests = db.Column(db.Text)  # JSON string
    skills = db.Column(db.Text)  # JSON string
    coding_ability = db.Column(db.String(20))  # beginner, intermediate, advanced
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    performances = db.relationship('Performance', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    chat_history = db.relationship('ChatHistory', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self, include_performance=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'roll_number': self.roll_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'phone': self.phone,
            'department': self.department,
            'semester': self.semester,
            'batch': self.batch,
            'section': self.section,
            'current_cgpa': self.current_cgpa,
            'family_income': self.family_income,
            'parent_name': self.parent_name,
            'parent_phone': self.parent_phone,
            'parent_email': self.parent_email,
            'interests': self.interests,
            'skills': self.skills,
            'coding_ability': self.coding_ability,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_performance:
            from app.models.performance import Performance
            latest_performance = self.performances.order_by(Performance.created_at.desc()).first()
            if latest_performance:
                data['latest_performance'] = latest_performance.to_dict()
        
        return data
    
    def __repr__(self):
        return f'<Student {self.roll_number} - {self.full_name}>'
