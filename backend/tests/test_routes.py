"""
Unit tests for API routes
"""
import pytest
import json
from app import create_app, db
from app.models.user import User
from app.models.student import Student

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return auth headers"""
    # Create test user
    user = User(
        email='test@example.com',
        username='testuser',
        role='student',
        is_active=True
    )
    user.set_password('password123')
    
    db.session.add(user)
    db.session.commit()
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    data = json.loads(response.data)
    token = data['access_token']
    
    return {'Authorization': f'Bearer {token}'}

def test_register(client):
    """Test user registration"""
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'username': 'newuser',
        'password': 'password123',
        'role': 'student'
    })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data

def test_login(client, auth_headers):
    """Test user login"""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_get_current_user(client, auth_headers):
    """Test get current user endpoint"""
    response = client.get('/api/auth/me', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'testuser'

def test_unauthorized_access(client):
    """Test unauthorized access"""
    response = client.get('/api/auth/me')
    
    assert response.status_code == 401
