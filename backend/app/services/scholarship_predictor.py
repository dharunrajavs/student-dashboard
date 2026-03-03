"""
ML Service for Scholarship Eligibility Prediction
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

class ScholarshipPredictorService:
    """Service for predicting scholarship eligibility"""
    
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = model_path
        
        if model_path and os.path.exists(model_path):
            self.load_model()
        else:
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
    
    def prepare_features(self, data):
        """
        Prepare features for prediction
        Input features:
        - gpa (0-10)
        - attendance_percentage (0-100)
        - family_income (in thousands)
        - extracurricular_score (0-100)
        - discipline_score (0-100)
        - research_publications (count)
        """
        features = np.array([[
            data.get('gpa', 0),
            data.get('attendance_percentage', 0),
            data.get('family_income', 0) / 1000,  # Normalize income
            data.get('extracurricular_score', 0),
            data.get('discipline_score', 100),
            data.get('research_publications', 0)
        ]])
        
        return features
    
    def predict(self, data):
        """
        Predict scholarship eligibility
        Returns: dict with eligible status, probability, missing criteria
        """
        if self.model is None:
            return self._rule_based_prediction(data)
        
        try:
            features = self.prepare_features(data)
            features_scaled = self.scaler.transform(features)
            
            # Predict probability
            probability = self.model.predict_proba(features_scaled)[0]
            eligible = probability[1] > 0.5
            
            return {
                'eligible': bool(eligible),
                'probability': round(float(probability[1]) * 100, 2),
                'confidence_score': round(max(probability) * 100, 2),
                'missing_criteria': self._get_missing_criteria(data),
                'recommendations': self._get_recommendations(data, eligible)
            }
        
        except Exception:
            return self._rule_based_prediction(data)
    
    def _rule_based_prediction(self, data):
        """Rule-based eligibility prediction"""
        score = 0
        max_score = 100
        
        # GPA criteria (30 points)
        gpa = data.get('gpa', 0)
        if gpa >= 8.5:
            score += 30
        elif gpa >= 7.5:
            score += 20
        elif gpa >= 6.5:
            score += 10
        
        # Attendance criteria (20 points)
        attendance = data.get('attendance_percentage', 0)
        if attendance >= 90:
            score += 20
        elif attendance >= 80:
            score += 15
        elif attendance >= 75:
            score += 10
        
        # Financial need (20 points)
        income = data.get('family_income', 0)
        if income < 300000:  # Less than 3 lakhs
            score += 20
        elif income < 500000:  # Less than 5 lakhs
            score += 15
        elif income < 800000:  # Less than 8 lakhs
            score += 10
        
        # Extracurricular (15 points)
        extra_score = data.get('extracurricular_score', 0)
        score += min(15, extra_score * 0.15)
        
        # Discipline (10 points)
        discipline = data.get('discipline_score', 100)
        score += min(10, discipline * 0.1)
        
        # Research (5 points)
        publications = data.get('research_publications', 0)
        score += min(5, publications * 2)
        
        probability = (score / max_score) * 100
        eligible = probability >= 60
        
        return {
            'eligible': eligible,
            'probability': round(probability, 2),
            'confidence_score': round(min(95, probability + 10), 2),
            'missing_criteria': self._get_missing_criteria(data),
            'recommendations': self._get_recommendations(data, eligible),
            'score_breakdown': {
                'gpa_score': min(30, gpa * 3),
                'attendance_score': min(20, attendance * 0.2),
                'financial_score': self._calculate_financial_score(income),
                'extracurricular_score': min(15, extra_score * 0.15),
                'discipline_score': min(10, discipline * 0.1),
                'research_score': min(5, publications * 2)
            }
        }
    
    def _calculate_financial_score(self, income):
        """Calculate financial need score"""
        if income < 300000:
            return 20
        elif income < 500000:
            return 15
        elif income < 800000:
            return 10
        return 0
    
    def _get_missing_criteria(self, data):
        """Identify missing or weak criteria"""
        missing = []
        
        if data.get('gpa', 0) < 7.5:
            missing.append({
                'criterion': 'Academic Performance',
                'current': data.get('gpa', 0),
                'required': 7.5,
                'impact': 'High'
            })
        
        if data.get('attendance_percentage', 0) < 75:
            missing.append({
                'criterion': 'Attendance',
                'current': data.get('attendance_percentage', 0),
                'required': 75,
                'impact': 'High'
            })
        
        if data.get('extracurricular_score', 0) < 50:
            missing.append({
                'criterion': 'Extracurricular Activities',
                'current': data.get('extracurricular_score', 0),
                'required': 50,
                'impact': 'Medium'
            })
        
        if data.get('discipline_score', 100) < 90:
            missing.append({
                'criterion': 'Discipline Record',
                'current': data.get('discipline_score', 100),
                'required': 90,
                'impact': 'Medium'
            })
        
        return missing
    
    def _get_recommendations(self, data, eligible):
        """Get personalized recommendations"""
        recommendations = []
        
        if eligible:
            recommendations.append("You meet the scholarship criteria! Prepare your application.")
            recommendations.append("Gather recommendation letters from faculty.")
            recommendations.append("Prepare a statement of purpose highlighting your achievements.")
        else:
            recommendations.append("Focus on improving your GPA through consistent study.")
            
            if data.get('attendance_percentage', 0) < 75:
                recommendations.append("Improve attendance to meet minimum requirements.")
            
            if data.get('extracurricular_score', 0) < 50:
                recommendations.append("Participate in extracurricular activities and competitions.")
            
            recommendations.append("Seek guidance from scholarship coordinators.")
        
        return recommendations
    
    def train(self, X_train, y_train):
        """Train the model"""
        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)
        self.model.fit(X_train_scaled, y_train)
    
    def save_model(self, path=None):
        """Save model to disk"""
        save_path = path or self.model_path
        if save_path:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, save_path)
    
    def load_model(self, path=None):
        """Load model from disk"""
        load_path = path or self.model_path
        if load_path and os.path.exists(load_path):
            saved_data = joblib.load(load_path)
            self.model = saved_data['model']
            self.scaler = saved_data['scaler']


# Singleton instance
scholarship_predictor_service = ScholarshipPredictorService()
