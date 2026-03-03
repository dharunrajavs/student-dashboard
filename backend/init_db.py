"""
Database initialization script
"""
from app import create_app, db
from app.models.user import User
from app.models.student import Student
from app.models.performance import Performance, ChatHistory, Prediction, Alert
import os

def init_database():
    """Initialize database with tables and sample data"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        print('Creating database tables...')
        db.create_all()
        print('✓ Tables created successfully')
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print('Creating admin user...')
            admin = User(
                email='admin@academicai.com',
                username='admin',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('✓ Admin user created (username: admin, password: admin123)')
        
        # Create sample student
        sample_student_user = User.query.filter_by(username='student1').first()
        if not sample_student_user:
            print('Creating sample student...')
            sample_student_user = User(
                email='student1@example.com',
                username='student1',
                role='student',
                is_active=True
            )
            sample_student_user.set_password('password')
            db.session.add(sample_student_user)
            db.session.flush()
            
            sample_student = Student(
                user_id=sample_student_user.id,
                roll_number='CS2024001',
                first_name='John',
                last_name='Doe',
                department='Computer Science',
                semester=5,
                batch='2024',
                current_cgpa=7.5,
                coding_ability='intermediate',
                interests='AI, Web Development, Data Science',
                skills='Python, JavaScript, React',
                family_income=500000,
                phone='1234567890'
            )
            db.session.add(sample_student)
            db.session.flush()
            
            # Add sample performance data
            subjects = ['Data Structures', 'Algorithms', 'Database Management', 'Web Technologies']
            for i, subject in enumerate(subjects):
                performance = Performance(
                    student_id=sample_student.id,
                    semester=5,
                    subject_name=subject,
                    internal_marks=70 + i * 5,
                    external_marks=65 + i * 3,
                    total_marks=135 + i * 8,
                    attendance_percentage=82 + i * 2,
                    assignment_score=75 + i * 3,
                    lab_performance=78 + i * 2,
                    study_hours_per_week=20,
                    participation_score=75,
                    discipline_score=95,
                    academic_year='2024-25',
                    month=i + 1
                )
                performance.grade = 'A' if performance.total_marks >= 140 else 'B+'
                db.session.add(performance)
            
            db.session.commit()
            print('✓ Sample student created (username: student1, password: password)')
        
        print('\n' + '='*50)
        print('Database initialization completed successfully!')
        print('='*50)
        print('\nDefault credentials:')
        print('Admin - Username: admin, Password: admin123')
        print('Student - Username: student1, Password: password')
        print('='*50)

if __name__ == '__main__':
    init_database()
