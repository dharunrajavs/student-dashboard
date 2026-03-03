"""
Unit tests for ML services
"""
import pytest
import numpy as np
from app.services.gpa_predictor import gpa_predictor_service
from app.services.scholarship_predictor import scholarship_predictor_service
from app.services.career_recommender import career_recommender_service
from app.services.risk_scorer import risk_scorer_service

def test_gpa_prediction():
    """Test GPA prediction"""
    result = gpa_predictor_service.predict(
        internal_marks=85,
        attendance=90,
        assignment_score=80,
        lab_performance=88,
        previous_gpa=8.5,
        study_hours=25,
        participation_score=85
    )
    
    assert 'predicted_gpa' in result
    assert 'confidence' in result
    assert 'grade' in result
    assert 'recommendations' in result
    assert 0 <= result['predicted_gpa'] <= 10

def test_scholarship_prediction():
    """Test scholarship prediction"""
    result = scholarship_predictor_service.predict(
        gpa=8.5,
        attendance=92,
        family_income=300000,
        extracurricular_score=85,
        discipline_score=95,
        publications=2
    )
    
    assert 'eligible' in result
    assert 'probability' in result
    assert 'score' in result
    assert 'criteria_met' in result
    assert isinstance(result['eligible'], bool)

def test_career_recommendation():
    """Test career recommendation"""
    result = career_recommender_service.recommend_careers(
        gpa=8.2,
        interests='AI, Machine Learning, Data Science',
        skills='Python, TensorFlow, SQL',
        coding_ability='advanced',
        projects=['Chatbot', 'Image Classification']
    )
    
    assert 'careers' in result
    assert len(result['careers']) > 0
    assert 'title' in result['careers'][0]
    assert 'match_score' in result['careers'][0]

def test_risk_scoring():
    """Test risk scoring"""
    result = risk_scorer_service.calculate_risk_score(
        current_gpa=6.5,
        attendance=70,
        performance_trend=[65, 68, 70, 72],
        assignment_completion=75,
        study_hours=15,
        discipline_score=80
    )
    
    assert 'risk_score' in result
    assert 'risk_level' in result
    assert 'factors' in result
    assert 'recommendations' in result
    assert 0 <= result['risk_score'] <= 100

def test_risk_levels():
    """Test different risk levels"""
    # Low risk
    low_risk = risk_scorer_service.calculate_risk_score(
        current_gpa=9.0,
        attendance=95,
        performance_trend=[85, 87, 90, 92],
        assignment_completion=95,
        study_hours=30,
        discipline_score=98
    )
    assert low_risk['risk_level'] in ['Minimal', 'Low']
    
    # High risk
    high_risk = risk_scorer_service.calculate_risk_score(
        current_gpa=5.5,
        attendance=60,
        performance_trend=[70, 65, 60, 55],
        assignment_completion=50,
        study_hours=8,
        discipline_score=60
    )
    assert high_risk['risk_level'] in ['High', 'Critical']
