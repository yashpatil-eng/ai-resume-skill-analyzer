# Backend - AI Career Intelligence Platform

## Overview
FastAPI backend for the AI-Driven Career Intelligence & Employability Platform.

## Features
- User authentication (JWT-based)
- Resume PDF parsing
- Skill extraction using NLP
- Job recommendations using ML (TF-IDF + Cosine Similarity)
- Skill gap analysis

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the `backend/` directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
```

### 3. Run the Server
```bash
# From backend directory
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info

### Resume
- `POST /api/v1/resume/upload` - Upload and process resume PDF
- `POST /api/v1/resume/extract-skills` - Extract skills from text

### Job Recommendations
- `POST /api/v1/jobs/recommend` - Get job recommendations
- `GET /api/v1/jobs/skill-gap/{job_id}` - Get skill gap analysis

## API Documentation
Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── core/
│   │   └── config.py        # Configuration settings
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   ├── resume.py        # Resume processing routes
│   │   └── recommend.py     # Job recommendation routes
│   ├── services/
│   │   ├── resume_parser.py # PDF parsing service
│   │   ├── skill_extractor.py # Skill extraction service
│   │   └── recommender.py   # ML recommendation service
│   └── models/
│       └── schemas.py       # Pydantic schemas
├── requirements.txt
└── README.md
```






