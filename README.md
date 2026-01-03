# AI-Driven Career Intelligence & Employability Platform

## 🎯 Project Overview

A comprehensive full-stack web application that leverages AI and Machine Learning to help job seekers:
- **Upload and analyze resumes** (PDF parsing)
- **Extract skills** using NLP techniques
- **Get personalized job recommendations** using ML algorithms
- **Identify skill gaps** to improve employability

This project is designed for:
- ✅ CSRBOX Applied AI Internship
- ✅ BTech Final Year Project
- ✅ Placement-level portfolio demonstration

## 🎓 SDG-8 Mapping: Decent Work and Economic Growth

This platform directly contributes to **UN Sustainable Development Goal 8** by:
- **Enhancing employability** through skill gap identification
- **Connecting job seekers** with suitable opportunities
- **Reducing unemployment** by matching skills to job requirements
- **Promoting economic growth** through better job-market alignment
- **Supporting career development** with data-driven insights

## 🚀 Features

### Core Functionality
1. **User Authentication**
   - Secure registration and login
   - JWT-based token authentication
   - Session management

2. **Resume Processing**
   - PDF upload and parsing
   - Automatic text extraction
   - Skill extraction using NLP

3. **AI-Powered Job Recommendations**
   - ML-based job matching (TF-IDF + Cosine Similarity)
   - Match percentage calculation
   - Ranked recommendations

4. **Skill Gap Analysis**
   - Identify missing skills for each job
   - Visual skill gap indicators
   - Actionable insights

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **CSS** - Custom styling

### Backend
- **FastAPI** - Modern Python web framework
- **PyPDF2** - PDF parsing
- **scikit-learn** - ML algorithms
- **pandas** - Data manipulation
- **numpy** - Numerical computations
- **python-jose** - JWT authentication
- **Pydantic** - Data validation

### AI/ML
- **TF-IDF Vectorization** - Text feature extraction
- **Cosine Similarity** - Job matching algorithm
- **NLP Keyword Matching** - Skill extraction

### Database & Storage
- **In-memory storage** (Phase 1) - Can be upgraded to Supabase
- **CSV dataset** - Job listings

## 📁 Project Structure

```
ai-career-intelligence-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── core/
│   │   │   └── config.py           # Configuration
│   │   ├── routes/
│   │   │   ├── auth.py             # Authentication routes
│   │   │   ├── resume.py           # Resume processing routes
│   │   │   └── recommend.py        # Job recommendation routes
│   │   ├── services/
│   │   │   ├── resume_parser.py    # PDF parsing service
│   │   │   ├── skill_extractor.py  # Skill extraction service
│   │   │   └── recommender.py      # ML recommendation service
│   │   └── models/
│   │       └── schemas.py          # Pydantic schemas
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx           # Login/Register page
│   │   │   └── Dashboard.jsx       # Main dashboard
│   │   ├── components/
│   │   │   ├── ResumeUpload.jsx    # Resume upload component
│   │   │   └── JobResults.jsx      # Job recommendations display
│   │   ├── services/
│   │   │   └── api.js              # API service
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── dataset/
│   └── jobs.csv                    # Job listings dataset
│
├── docs/
│   └── architecture.md             # System architecture documentation
│
└── README.md
```

## 🏃 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   python -m app.main
   # Or
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: `http://localhost:8000`
   API docs at: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at: `http://localhost:3000`

### Environment Variables (Optional)

Create a `.env` file in the `backend/` directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
```

## 📖 Usage Guide

### 1. Register/Login
- Navigate to the login page
- Register a new account or login with existing credentials
- JWT token will be stored automatically

### 2. Upload Resume
- Go to Dashboard
- Click "Choose PDF Resume" and select your resume PDF
- Click "Upload & Extract Skills"
- View extracted skills

### 3. Get Job Recommendations
- After skills are extracted, click "Get Job Recommendations"
- View ranked job recommendations with:
  - Match percentage
  - Required skills
  - Missing skills
  - Skill gap analysis

## 🧪 Testing the Application

### Test User Flow
1. Register a new account
2. Upload a sample PDF resume (create one with skills like: Python, JavaScript, React, SQL)
3. View extracted skills
4. Get job recommendations
5. Analyze skill gaps for each recommendation

### Sample Resume Content
Create a PDF with text like:
```
John Doe
Software Developer

Skills:
- Python
- JavaScript
- React
- SQL
- Git
- AWS

Experience:
- Developed web applications using React and Python
- Worked with databases like PostgreSQL and MongoDB
```

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

#### Resume
- `POST /api/v1/resume/upload` - Upload and process resume
- `POST /api/v1/resume/extract-skills` - Extract skills from text

#### Job Recommendations
- `POST /api/v1/jobs/recommend` - Get job recommendations
- `GET /api/v1/jobs/skill-gap/{job_id}` - Get skill gap analysis

## 🚀 Deployment

### Frontend (Vercel)
1. Push code to GitHub
2. Connect repository to Vercel
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Deploy

### Backend (Render)
1. Create new Web Service on Render
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Deploy

### Database (Supabase)
1. Create Supabase project
2. Update `DATABASE_URL` in backend config
3. Migrate user storage to PostgreSQL
4. Update job dataset to database table

## 🎓 Project Highlights for Viva

### Technical Implementation
- **Clean Architecture**: Separation of concerns (routes, services, models)
- **RESTful API Design**: Standard HTTP methods and status codes
- **ML Pipeline**: TF-IDF vectorization + Cosine Similarity
- **NLP Processing**: Skill extraction from unstructured text
- **Security**: JWT authentication, input validation

### AI/ML Components
- **Resume Parsing**: PDF text extraction
- **Skill Extraction**: NLP keyword matching with comprehensive skill dictionary
- **Job Matching**: TF-IDF + Cosine Similarity for semantic matching
- **Skill Gap Analysis**: Set-based comparison for missing skills

### Code Quality
- **Well-commented code**: Easy to explain in viva
- **Modular design**: Reusable services
- **Error handling**: Comprehensive try-catch blocks
- **Type validation**: Pydantic schemas for all inputs

## 📈 Future Enhancements

1. **Advanced NLP**: Transformer models for better skill extraction
2. **User Profiles**: Store resume history and preferences
3. **Learning Paths**: Recommend courses to fill skill gaps
4. **Real-time Updates**: WebSocket for live recommendations
5. **Multi-language Support**: Support for multiple languages
6. **Job Application Tracking**: Track applied jobs
7. **Resume Builder**: AI-powered resume creation tool

## 🤝 Contributing

This is a final year project. For improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Author

Created for:
- CSRBOX Applied AI Internship
- BTech Final Year Project
- Portfolio demonstration

## 🙏 Acknowledgments

- FastAPI community
- React team
- scikit-learn developers
- All open-source contributors

---

**Built with ❤️ for better employability and career growth**






