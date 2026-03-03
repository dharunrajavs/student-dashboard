"""
ML Service for GPA Prediction
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

class GPAPredictorService:
    """Service for predicting semester GPA"""
    
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = model_path
        
        if model_path and os.path.exists(model_path):
            self.load_model()
        else:
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
    
    def prepare_features(self, data):
        """
        Prepare features for prediction
        Input features:
        - internal_marks (0-100)
        - attendance_percentage (0-100)
        - assignment_score (0-100)
        - lab_performance (0-100)
        - previous_gpa (0-10)
        - study_hours_per_week (0-100)
        - participation_score (0-100)
        """
        features = np.array([[
            data.get('internal_marks', 0),
            data.get('attendance_percentage', 0),
            data.get('assignment_score', 0),
            data.get('lab_performance', 0),
            data.get('previous_gpa', 0),
            data.get('study_hours_per_week', 0),
            data.get('participation_score', 0)
        ]])
        
        return features
    
    def predict(self, data):
        """
        Predict semester GPA
        Returns: dict with predicted_gpa, confidence_score, grade_category
        """
        features = self.prepare_features(data)
        
        if self.model is None:
            # Use rule-based prediction if model not trained
            return self._rule_based_prediction(data)
        
        try:
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict
            predicted_gpa = self.model.predict(features_scaled)[0]
            
            # Ensure GPA is within valid range (0-10)
            predicted_gpa = max(0, min(10, predicted_gpa))
            
            # Calculate confidence score based on input quality
            confidence = self._calculate_confidence(data)
            
            # Determine grade category
            grade_category = self._get_grade_category(predicted_gpa)
            
            return {
                'predicted_gpa': round(predicted_gpa, 2),
                'confidence_score': round(confidence, 2),
                'grade_category': grade_category,
                'interpretation': self._get_interpretation(predicted_gpa),
                'recommendations': self._get_recommendations(predicted_gpa, data)
            }
        
        except Exception as e:
            return self._rule_based_prediction(data)
    
    def _rule_based_prediction(self, data):
        """Rule-based GPA prediction (fallback)"""
        # Weighted average approach
        internal = data.get('internal_marks', 0) / 10  # Convert to GPA scale
        attendance = data.get('attendance_percentage', 0) / 10
        assignment = data.get('assignment_score', 0) / 10
        lab = data.get('lab_performance', 0) / 10
        previous = data.get('previous_gpa', 0)
        study_hours = min(data.get('study_hours_per_week', 0), 40) / 4  # Max 40 hours
        participation = data.get('participation_score', 0) / 10
        
        # Weighted calculation
        predicted_gpa = (
            internal * 0.30 +
            attendance * 0.15 +
            assignment * 0.15 +
            lab * 0.15 +
            previous * 0.15 +
            study_hours * 0.05 +
            participation * 0.05
        )
        
        predicted_gpa = max(0, min(10, predicted_gpa))
        
        confidence = self._calculate_confidence(data)
        grade_category = self._get_grade_category(predicted_gpa)
        
        return {
            'predicted_gpa': round(predicted_gpa, 2),
            'confidence_score': round(confidence, 2),
            'grade_category': grade_category,
            'interpretation': self._get_interpretation(predicted_gpa),
            'recommendations': self._get_recommendations(predicted_gpa, data)
        }
    
    def _calculate_confidence(self, data):
        """Calculate prediction confidence based on data quality"""
        confidence = 100.0
        
        # Reduce confidence if key metrics are missing or low quality
        if data.get('previous_gpa', 0) == 0:
            confidence -= 15
        
        if data.get('attendance_percentage', 0) < 50:
            confidence -= 10
        
        if data.get('study_hours_per_week', 0) < 5:
            confidence -= 10
        
        return max(50, confidence)
    
    def _get_grade_category(self, gpa):
        """Get grade category based on GPA"""
        if gpa >= 9.0:
            return 'Outstanding (O)'
        elif gpa >= 8.0:
            return 'Excellent (A+)'
        elif gpa >= 7.0:
            return 'Very Good (A)'
        elif gpa >= 6.0:
            return 'Good (B)'
        elif gpa >= 5.0:
            return 'Average (C)'
        else:
            return 'Below Average (D)'
    
    def _get_interpretation(self, gpa):
        """Get interpretation of predicted GPA"""
        if gpa >= 8.5:
            return "Excellent performance! You're on track for top grades."
        elif gpa >= 7.0:
            return "Very good performance! Keep up the great work."
        elif gpa >= 6.0:
            return "Good performance. There's room for improvement."
        elif gpa >= 5.0:
            return "Average performance. Focus on weak areas to improve."
        else:
            return "Performance needs improvement. Seek help and work harder."
    
    def _get_recommendations(self, gpa, data):
        """Get personalized recommendations"""
        recommendations = []
        
        if gpa < 7.0:
            if data.get('attendance_percentage', 0) < 75:
                recommendations.append("Improve attendance to at least 75%")
            
            if data.get('study_hours_per_week', 0) < 20:
                recommendations.append("Increase study hours to at least 20 hours per week")
            
            if data.get('assignment_score', 0) < 70:
                recommendations.append("Focus on completing assignments with better quality")
            
            if data.get('lab_performance', 0) < 70:
                recommendations.append("Improve lab participation and practical skills")
        
        if not recommendations:
            recommendations.append("Maintain your current performance level")
            recommendations.append("Consider participating in advanced projects")
        
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
gpa_predictor_service = GPAPredictorService()
