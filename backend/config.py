import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    """Get database URL, fixing Render's postgres:// to postgresql://"""
    url = os.getenv('DATABASE_URL', 'sqlite:///academic_intelligence.db')
    # Render uses postgres:// but SQLAlchemy requires postgresql://
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    return url

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # Database
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 1800,
        'pool_pre_ping': True
    }
    
    # Cache - Use simple cache by default (no Redis required)
    REDIS_URL = os.getenv('REDIS_URL')
    CACHE_TYPE = 'redis' if os.getenv('REDIS_URL') else 'SimpleCache'
    CACHE_REDIS_URL = os.getenv('REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_TTL', 300))
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000)))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', 500))
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', 0.7))
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@academicai.com')
    
    # File Upload
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 10485760))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'pdf,png,jpg,jpeg,xls,xlsx,csv').split(','))
    
    # CORS - Allow multiple ports for development and production domains
    CORS_ORIGINS = [o.strip() for o in os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004,http://localhost:3005').split(',') if o.strip()]
    
    # Rate Limiting - Use memory storage if no Redis
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    
    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 100))
    
    # ML Models
    GPA_MODEL_PATH = os.getenv('GPA_MODEL_PATH', 'ml_models/gpa_predictor.pkl')
    SCHOLARSHIP_MODEL_PATH = os.getenv('SCHOLARSHIP_MODEL_PATH', 'ml_models/scholarship_classifier.pkl')
    CAREER_MODEL_PATH = os.getenv('CAREER_MODEL_PATH', 'ml_models/career_recommender.pkl')
    RISK_MODEL_PATH = os.getenv('RISK_MODEL_PATH', 'ml_models/risk_scorer.pkl')
    
    # Reports
    REPORTS_FOLDER = os.getenv('REPORTS_FOLDER', 'reports')
    LOGO_PATH = os.getenv('LOGO_PATH', 'static/logo.png')
    
    # URLs
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')
    
    # Thresholds
    LOW_ATTENDANCE_THRESHOLD = float(os.getenv('LOW_ATTENDANCE_THRESHOLD', 75))
    LOW_GPA_THRESHOLD = float(os.getenv('LOW_GPA_THRESHOLD', 6.0))
    HIGH_RISK_THRESHOLD = float(os.getenv('HIGH_RISK_THRESHOLD', 70))
    
    # Notifications
    ENABLE_EMAIL_NOTIFICATIONS = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'True') == 'True'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use simpler pool settings for production free tier
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 3,
        'pool_recycle': 1800,
        'pool_pre_ping': True,
        'max_overflow': 2
    }


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
