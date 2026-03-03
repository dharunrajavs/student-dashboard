"""
Services Module
"""
from app.services.gpa_predictor import gpa_predictor_service
from app.services.scholarship_predictor import scholarship_predictor_service
from app.services.career_recommender import career_recommendation_service
from app.services.risk_scorer import risk_scoring_service
from app.services.chatbot import chatbot_service
from app.services.email_service import email_service
from app.services.pdf_generator import pdf_generator

__all__ = [
    'gpa_predictor_service',
    'scholarship_predictor_service', 
    'career_recommendation_service',
    'risk_scoring_service',
    'chatbot_service',
    'email_service',
    'pdf_generator'
]
