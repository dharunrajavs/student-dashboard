from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flasgger import Swagger
import logging
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    storage_uri="memory://"  # Default to memory, will be overridden by config
)

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # JWT callbacks for handling user identity
    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        """Convert user_id to string for JWT"""
        return str(user_id)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Load user from JWT identity"""
        from app.models.user import User
        identity = jwt_data["sub"]
        return User.query.get(int(identity))
    
    mail.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Configure Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "AI Academic Intelligence Platform API",
            "description": "REST API for AI-powered student performance prediction and academic guidance",
            "version": "1.0.0",
            "contact": {
                "name": "DHARUNRAJA V",
                "email": "support@academicai.com"
            }
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [{"Bearer": []}]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Setup logging
    setup_logging(app)
    
    # Create necessary directories
    create_directories(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register shell context
    @app.shell_context_processor
    def make_shell_context():
        from app.models.user import User
        from app.models.student import Student
        from app.models.performance import Performance
        return {
            'db': db,
            'User': User,
            'Student': Student,
            'Performance': Performance
        }
    
    return app


def setup_logging(app):
    """Configure application logging"""
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.FileHandler(app.config['LOG_FILE'])
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.info('Academic Intelligence Platform startup')


def create_directories(app):
    """Create necessary directories"""
    directories = [
        app.config['UPLOAD_FOLDER'],
        app.config['REPORTS_FOLDER'],
        'logs',
        'ml_models',
        'static'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def register_blueprints(app):
    """Register application blueprints"""
    from app.routes import auth, students, predictions, chatbot, analytics, admin, reports
    
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(students.bp, url_prefix='/api/students')
    app.register_blueprint(predictions.bp, url_prefix='/api/predict')
    app.register_blueprint(chatbot.bp, url_prefix='/api/chatbot')
    app.register_blueprint(analytics.bp, url_prefix='/api/analytics')
    app.register_blueprint(admin.bp, url_prefix='/api/admin')
    app.register_blueprint(reports.reports, url_prefix='/api/reports')


def register_error_handlers(app):
    """Register error handlers"""
    from flask import jsonify
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden', 'message': 'Insufficient permissions'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Internal server error: {error}')
        return jsonify({'error': 'Internal server error', 'message': 'Something went wrong'}), 500
