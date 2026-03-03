# 🎓 AI Academic Intelligence Platform

A next-generation AI-powered student performance prediction and academic guidance system with advanced ML models, chatbot mentor, and comprehensive analytics.

## 🚀 Features

### Core Features
- **AI Chatbot Mentor** - Context-aware chatbot using OpenAI API for personalized academic guidance
- **Semester GPA Predictor** - ML regression model predicting student GPA with confidence scores
- **Performance Heatmap** - Visual analytics showing subject-wise performance trends
- **Scholarship Eligibility Predictor** - Classification model for scholarship recommendations
- **Career Recommendation System** - AI-powered career path suggestions based on academic profile
- **Risk Scoring System** - Early warning system for at-risk students (0-100 scale)

### Premium Features
- Real-time email notifications
- PDF academic report generator
- Student leaderboard and ranking
- Admin analytics dashboard
- Dark/Light theme support
- Role-based access control (Admin/Student/Faculty)
- Mobile-responsive design

## 🏗️ Architecture

```
ai-academic-platform/
├── backend/                 # Flask REST API
│   ├── app/
│   │   ├── models/         # ML models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utilities
│   │   └── __init__.py
│   ├── ml_models/          # Trained models
│   ├── config.py
│   └── run.py
├── frontend/               # React application
│   ├── public/
│   └── src/
│       ├── components/     # Reusable components
│       ├── pages/          # Page components
│       ├── services/       # API services
│       ├── styles/         # CSS/SCSS
│       └── utils/
├── database/               # Database scripts
├── docker/                 # Docker configs
└── docs/                   # Documentation
```

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis (for caching)
- Docker & Docker Compose (optional)

## 🔧 Installation

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-academic-platform
```

2. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configurations
```

5. **Initialize database**
```bash
python init_db.py
```

6. **Train ML models**
```bash
python train_models.py
```

7. **Run backend server**
```bash
python run.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with API URL
```

3. **Run development server**
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
docker-compose up -d
```

This will start:
- Backend API (port 5000)
- Frontend (port 3000)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)

## 📊 API Documentation

Access Swagger documentation at: `http://localhost:5000/api/docs`

### Key Endpoints

#### Student APIs
- `POST /api/students/register` - Register new student
- `GET /api/students/{id}/profile` - Get student profile
- `GET /api/students/{id}/performance` - Get performance analytics

#### Prediction APIs
- `POST /api/predict/gpa` - Predict semester GPA
- `POST /api/predict/scholarship` - Check scholarship eligibility
- `POST /api/predict/career` - Get career recommendations
- `GET /api/predict/risk-score/{student_id}` - Calculate risk score

#### Chatbot APIs
- `POST /api/chatbot/message` - Send message to AI mentor
- `GET /api/chatbot/history/{student_id}` - Get chat history

#### Analytics APIs
- `GET /api/analytics/heatmap/{student_id}` - Performance heatmap data
- `GET /api/analytics/trends/{student_id}` - Performance trends
- `GET /api/analytics/leaderboard` - Student rankings

#### Admin APIs
- `GET /api/admin/dashboard` - Admin analytics
- `GET /api/admin/students/at-risk` - List at-risk students
- `GET /api/admin/scholarships/eligible` - Export eligible students
- `POST /api/admin/reports/generate` - Generate PDF reports

## 🔑 Environment Variables

### Backend (.env)
```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/academic_db

# Redis
REDIS_URL=redis://localhost:6379/0

# OpenAI API
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=3600

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_FOLDER=uploads
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

## 🧪 Testing

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

## 📱 Features Overview

### 1. AI Chatbot Mentor
- Context-aware conversations using OpenAI GPT-4
- Personalized study plans
- Subject-wise improvement strategies
- Academic query resolution
- Student motivation and guidance
- Chat history persistence

### 2. Semester GPA Predictor
- ML regression model with high accuracy
- Inputs: Internal marks, attendance, assignments, lab scores, study hours
- Outputs: Predicted GPA, confidence score, grade category
- Visual speedometer-style GPA meter
- Comparison with class average
- Trend analysis

### 3. Performance Heatmap
- Subject vs performance visualization
- Attendance vs marks correlation
- Monthly performance trends
- Color-coded risk levels (Green/Yellow/Red)
- Interactive charts using Recharts

### 4. Scholarship Eligibility Predictor
- Classification model for scholarship prediction
- Multi-factor analysis (GPA, attendance, income, activities)
- Probability scores
- Missing criteria suggestions
- Admin export to Excel

### 5. Career Recommendation System
- AI-powered career path suggestions
- Based on: Subject strengths, GPA, interests, skills
- Outputs: Career roles, required skills, courses, salary estimates
- Detailed AI explanations

### 6. Risk Scoring System
- 0-100 risk score calculation
- Early warning system
- Email alerts to students and faculty
- Intervention recommendations

## 🎨 UI/UX Features

- Modern SaaS-style dashboard
- Glassmorphism design
- Animated charts and transitions
- Clean sidebar navigation
- Fully responsive (mobile/tablet/desktop)
- Dark/Light theme toggle
- Professional color palette
- Smooth animations

## 👥 User Roles

1. **Student**
   - View personal dashboard
   - Check predictions
   - Chat with AI mentor
   - View performance analytics
   - Download reports

2. **Faculty**
   - View student performance
   - Identify at-risk students
   - Monitor class analytics
   - Generate reports

3. **Admin**
   - Full system access
   - User management
   - System analytics
   - Export capabilities
   - Configuration management

## 🔒 Security Features

- JWT-based authentication
- Password hashing (bcrypt)
- API rate limiting
- CORS protection
- SQL injection prevention
- XSS protection
- Environment variable secrets

## 📈 Performance Optimizations

- Redis caching for frequent queries
- Database query optimization
- Lazy loading in frontend
- Code splitting
- Compressed assets
- CDN integration ready

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Developer

**DHARUNRAJA V**

## 🙏 Acknowledgments

- OpenAI for GPT API
- scikit-learn for ML models
- React community
- Flask community

## 📞 Support

For support, email: support@academicai.com

---

**⭐ Star this repository if you find it helpful!**

Built with ❤️ for better education
