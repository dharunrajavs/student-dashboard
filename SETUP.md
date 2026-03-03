# Comprehensive Setup Guide

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker Desktop installed
- OpenAI API key

### Steps

1. **Clone and Configure**
```bash
cd "c:\Users\DHARUNRAJA V\OneDrive\Desktop\my project"

# Create .env file
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

2. **Start All Services**
```bash
docker-compose up --build
```

3. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- API Documentation: http://localhost:5000/api/docs

4. **Default Credentials**
- Admin: `admin` / `admin123`
- Student: `student1` / `password`

---

## Manual Setup (Development)

### Backend Setup

1. **Install Python Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
copy .env.example .env
# Update DATABASE_URL, SECRET_KEY, OPENAI_API_KEY
```

3. **Initialize Database**
```bash
python init_db.py
```

4. **Train ML Models**
```bash
python train_models.py
```

5. **Run Backend**
```bash
# Development
python run.py

# Production
gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Configure Environment**
```bash
# Create .env file
echo REACT_APP_API_URL=http://localhost:5000/api > .env
```

3. **Run Frontend**
```bash
# Development
npm start

# Production build
npm run build
```

---

## Features Overview

### 🤖 AI Chatbot Mentor
- Powered by OpenAI GPT-4
- Personalized study plans
- Performance analysis
- 24/7 academic guidance

### 📊 ML Predictions
- **GPA Predictor**: Predict next semester GPA
- **Scholarship Eligibility**: ML-based classification
- **Career Recommender**: Best-fit career paths
- **Risk Scoring**: 0-100 scale with 6 risk factors

### 📈 Analytics
- Performance heatmap (Recharts)
- Subject-wise trends
- Class leaderboard
- Comparative analysis

### 🎓 Premium Features
- PDF report generation
- Email notifications
- Alert system
- Dark/Light theme
- Role-based access control (RBAC)

### 👨‍💼 Admin Panel
- Dashboard statistics
- At-risk student identification
- Scholarship export (Excel)
- Alert creation
- Student management

---

## API Endpoints

### Authentication
```
POST /api/auth/register       - Register new user
POST /api/auth/login          - Login
POST /api/auth/refresh        - Refresh JWT token
GET  /api/auth/me             - Get current user
PUT  /api/auth/change-password - Change password
```

### Students
```
GET    /api/students/profile        - Get student profile
PUT    /api/students/profile        - Update profile
GET    /api/students/performance    - Get performance records
POST   /api/students/performance    - Add performance record
GET    /api/students/all            - List all students (Admin)
```

### Predictions
```
POST /api/predict/gpa              - Predict GPA
POST /api/predict/scholarship      - Check scholarship eligibility
POST /api/predict/career           - Get career recommendations
POST /api/predict/risk-score       - Calculate risk score
```

### Chatbot
```
POST   /api/chatbot/message        - Send message to AI mentor
GET    /api/chatbot/history        - Get chat history
POST   /api/chatbot/study-plan     - Generate study plan
DELETE /api/chatbot/clear-history  - Clear chat history
```

### Analytics
```
GET /api/analytics/heatmap         - Performance heatmap data
GET /api/analytics/trends          - Performance trends
GET /api/analytics/leaderboard     - Class leaderboard
GET /api/analytics/comparison      - Class comparison stats
```

### Admin
```
GET  /api/admin/dashboard          - Dashboard statistics
GET  /api/admin/at-risk            - At-risk students
GET  /api/admin/scholarship-eligible - Scholarship eligible list
GET  /api/admin/export/scholarship - Export Excel
POST /api/admin/alerts             - Create alert
PUT  /api/admin/students/:id/deactivate - Deactivate student
```

### Reports
```
POST /api/reports/generate-pdf     - Generate PDF report
POST /api/reports/email-report     - Email PDF report
POST /api/reports/send-alert       - Send alert email (Admin)
```

---

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: PostgreSQL 15 (SQLAlchemy ORM)
- **Cache**: Redis 7
- **ML**: scikit-learn, pandas, numpy
- **AI**: OpenAI GPT-4
- **Auth**: Flask-JWT-Extended, bcrypt
- **API Docs**: Flasgger (Swagger)

### Frontend
- **Framework**: React 18.2.0
- **Router**: React Router v6
- **Charts**: Recharts 2.10.3
- **Styling**: styled-components, CSS3
- **Animations**: framer-motion
- **HTTP**: Axios
- **Notifications**: react-hot-toast

### DevOps
- **Containerization**: Docker, docker-compose
- **Web Server**: Nginx (frontend), Gunicorn (backend)
- **Testing**: pytest, React Testing Library

---

## Environment Variables

### Backend (.env)
```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/academic_intelligence_db

# Redis
REDIS_URL=redis://localhost:6379/0

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# CORS
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000/api
```

---

## Project Structure

```
my project/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # App factory
│   │   ├── models/               # Database models
│   │   │   ├── user.py
│   │   │   ├── student.py
│   │   │   └── performance.py
│   │   ├── routes/               # API blueprints
│   │   │   ├── auth.py
│   │   │   ├── students.py
│   │   │   ├── predictions.py
│   │   │   ├── chatbot.py
│   │   │   ├── analytics.py
│   │   │   ├── admin.py
│   │   │   └── reports.py
│   │   └── services/             # Business logic
│   │       ├── gpa_predictor.py
│   │       ├── scholarship_predictor.py
│   │       ├── career_recommender.py
│   │       ├── risk_scorer.py
│   │       ├── chatbot.py
│   │       ├── email_service.py
│   │       └── pdf_generator.py
│   ├── config.py                 # Configuration
│   ├── run.py                    # Entry point
│   ├── init_db.py                # DB initialization
│   ├── train_models.py           # ML model training
│   ├── requirements.txt          # Dependencies
│   └── Dockerfile
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/           # Reusable components
│   │   │   ├── Layout.js
│   │   │   └── PrivateRoute.js
│   │   ├── context/              # React contexts
│   │   │   ├── AuthContext.js
│   │   │   └── ThemeContext.js
│   │   ├── pages/                # Page components
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Dashboard.js
│   │   │   ├── StudentProfile.js
│   │   │   ├── Predictions.js
│   │   │   ├── Analytics.js
│   │   │   ├── ChatbotPage.js
│   │   │   └── AdminDashboard.js
│   │   ├── services/
│   │   │   └── api.js            # API service layer
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .env.example
├── README.md
└── SETUP.md (this file)
```

---

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## Deployment

### Docker Compose (Recommended)
```bash
# Production deployment
docker-compose -f docker-compose.yml up -d
```

### Manual Production Deployment

1. **Backend**
```bash
cd backend
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 run:app
```

2. **Frontend**
```bash
cd frontend
npm run build
# Serve build/ folder with Nginx
```

3. **Database**
```bash
# PostgreSQL on port 5432
# Redis on port 6379
```

---

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Run `python init_db.py` to create tables

### OpenAI API Errors
- Verify OPENAI_API_KEY is set
- Check API quota and billing
- Fallback: Bot uses rule-based responses

### Email Not Sending
- Enable "Less secure app access" for Gmail
- Use App Password instead of regular password
- Check SMTP settings in .env

### Frontend Build Errors
- Delete node_modules and package-lock.json
- Run `npm install` again
- Clear npm cache: `npm cache clean --force`

### Docker Issues
- Run `docker-compose down -v` to reset
- Delete volumes: `docker volume prune`
- Rebuild: `docker-compose up --build`

---

## Performance Optimization

1. **Backend**
   - Redis caching enabled (5-minute default)
   - Database connection pooling
   - Rate limiting (100 requests/hour)
   - Gzip compression

2. **Frontend**
   - Code splitting with React.lazy()
   - Image optimization
   - CSS minification
   - PWA ready

3. **Database**
   - Indexed columns (user_id, student_id)
   - Query optimization
   - Connection pooling

---

## Security Best Practices

1. **Change default secrets**
   - Update SECRET_KEY and JWT_SECRET_KEY
   - Use strong passwords

2. **Enable HTTPS**
   - Use SSL certificates
   - Update CORS_ORIGINS

3. **Rate Limiting**
   - Configured via Flask-Limiter
   - Adjust limits in config.py

4. **Input Validation**
   - All inputs sanitized
   - SQL injection prevention via ORM

---

## Support & Contact

- **Developer**: DHARUNRAJA V
- **Email**: support@academicai.com
- **Documentation**: http://localhost:5000/api/docs

---

## License

This project is created for educational and hackathon purposes.

---

## Next Steps

1. ✅ Setup development environment
2. ✅ Configure database and Redis
3. ✅ Add your OpenAI API key
4. ✅ Run `docker-compose up`
5. ✅ Access http://localhost:3000
6. ✅ Login with default credentials
7. ✅ Explore features and customize

**Happy Coding! 🚀**
