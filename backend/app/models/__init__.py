"""
Models Module
"""
from app.models.user import User
from app.models.student import Student
from app.models.performance import Performance, ChatHistory, Prediction, Alert

__all__ = ['User', 'Student', 'Performance', 'ChatHistory', 'Prediction', 'Alert']
