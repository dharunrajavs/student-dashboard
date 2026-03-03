"""
Script to train ML models with sample data
"""
import numpy as np
from app.services.gpa_predictor import gpa_predictor_service
from app.services.scholarship_predictor import scholarship_predictor_service
import os

def generate_sample_data(n_samples=500):
    """Generate synthetic training data"""
    np.random.seed(42)
    
    # GPA training data
    X_gpa = np.random.rand(n_samples, 7) * 100  # 7 features
    # Simple linear combination with noise
    y_gpa = (
        X_gpa[:, 0] * 0.03 +  # internal marks
        X_gpa[:, 1] * 0.015 +  # attendance
        X_gpa[:, 2] * 0.015 +  # assignment
        X_gpa[:, 3] * 0.015 +  # lab
        X_gpa[:, 4] * 0.15 +  # previous gpa (0-10 range)
        X_gpa[:, 5] * 0.005 +  # study hours
        X_gpa[:, 6] * 0.005 +  # participation
        np.random.randn(n_samples) * 0.5  # noise
    )
    y_gpa = np.clip(y_gpa, 0, 10)
    
    # Scholarship training data
    X_scholarship = np.random.rand(n_samples, 6)
    X_scholarship[:, 0] *= 10  # GPA 0-10
    X_scholarship[:, 1] *= 100  # Attendance 0-100
    X_scholarship[:, 2] *= 1000  # Income in thousands
    X_scholarship[:, 3] *= 100  # Extracurricular 0-100
    X_scholarship[:, 4] *= 100  # Discipline 0-100
    X_scholarship[:, 5] *= 5  # Publications 0-5
    
    # Eligibility: high GPA, good attendance, lower income
    y_scholarship = ((X_scholarship[:, 0] > 7) & 
                     (X_scholarship[:, 1] > 75) & 
                     (X_scholarship[:, 2] < 600)).astype(int)
    
    return X_gpa, y_gpa, X_scholarship, y_scholarship

def train_models():
    """Train all ML models"""
    print('Generating training data...')
    X_gpa, y_gpa, X_scholarship, y_scholarship = generate_sample_data()
    
    print('Training GPA Predictor...')
    gpa_predictor_service.train(X_gpa, y_gpa)
    os.makedirs('ml_models', exist_ok=True)
    gpa_predictor_service.save_model('ml_models/gpa_predictor.pkl')
    print('✓ GPA Predictor trained and saved')
    
    print('Training Scholarship Predictor...')
    scholarship_predictor_service.train(X_scholarship, y_scholarship)
    scholarship_predictor_service.save_model('ml_models/scholarship_classifier.pkl')
    print('✓ Scholarship Predictor trained and saved')
    
    print('\n' + '='*50)
    print('ML models trained successfully!')
    print('='*50)

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        train_models()
