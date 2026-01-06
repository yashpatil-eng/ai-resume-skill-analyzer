# System Architecture

## Overview
The AI-Driven Career Intelligence & Employability Platform is a full-stack web application that uses AI/ML techniques to analyze resumes, extract skills, and recommend suitable job opportunities.

## Architecture Diagram

```
┌─────────────────┐
│   React Frontend │
│   (Vite + Axios) │
└────────┬────────┘
         │ HTTP/REST API
         │
┌────────▼────────────────────────┐
│      FastAPI Backend            │
│  ┌──────────────────────────┐  │
│  │   Authentication Layer    │  │
│  │   (JWT-based)             │  │
│  └──────────────────────────┘  │
│  ┌──────────────────────────┐  │
│  │   Resume Processing       │  │
│  │   - PDF Parser            │  │
│  │   - Skill Extractor       │  │
│  └──────────────────────────┘  │
│  ┌──────────────────────────┐  │
│  │   ML Recommendation      │  │
│  │   - TF-IDF Vectorizer    │  │
│  │   - Cosine Similarity    │  │
│  │   - Skill Gap Analysis   │  │
│  └──────────────────────────┘  │
└────────────────────────────────┘
         │
         │
┌────────▼────────┐
│   Dataset       │
│   (jobs.csv)    │
└─────────────────┘
```

## Component Architecture

### Frontend (React + Vite)

#### Pages
- **Login.jsx**: User authentication (login/register)
- **Dashboard.jsx**: Main application interface

#### Components
- **ResumeUpload.jsx**: PDF upload and skill extraction display
- **JobResults.jsx**: Job recommendations with match scores and skill gaps

#### Services
- **api.js**: Axios-based API client with interceptors for authentication

### Backend (FastAPI)

#### Routes Layer
- **auth.py**: User registration, login, token management
- **resume.py**: Resume upload, PDF parsing, skill extraction
- **recommend.py**: Job recommendations, skill gap analysis

#### Services Layer
- **resume_parser.py**: PDF text extraction using PyPDF2
- **skill_extractor.py**: NLP-based skill extraction using keyword matching
- **recommender.py**: ML-based job recommendation using TF-IDF + Cosine Similarity

#### Models Layer
- **schemas.py**: Pydantic models for request/response validation

#### Core
- **config.py**: Application configuration and settings

## Data Flow

### 1. User Registration/Login
```
User → Frontend → POST /auth/register or /auth/login
     → Backend validates → Returns JWT token
     → Frontend stores token → Redirects to Dashboard
```

### 2. Resume Upload & Processing
```
User uploads PDF → Frontend → POST /resume/upload
                  → Backend:
                    1. Parse PDF (PyPDF2)
                    2. Extract text
                    3. Extract skills (NLP keyword matching)
                  → Returns extracted skills
                  → Frontend displays skills
```

### 3. Job Recommendation
```
User clicks "Get Recommendations" → Frontend → POST /jobs/recommend
                                  → Backend:
                                    1. Load jobs dataset
                                    2. Convert user skills to TF-IDF vector
                                    3. Calculate cosine similarity with all jobs
                                    4. Rank jobs by similarity
                                    5. Calculate skill gaps for each job
                                  → Returns ranked recommendations
                                  → Frontend displays results
```

## ML/AI Pipeline

### Skill Extraction
1. **Text Extraction**: PyPDF2 extracts text from PDF
2. **Text Normalization**: Lowercase, remove special characters
3. **Keyword Matching**: Match against predefined skill dictionary
4. **Skill Categorization**: Classify as technical or soft skills

### Job Recommendation
1. **Vectorization**: 
   - Combine job title + skills into text
   - Apply TF-IDF vectorization
   - Create vector for user skills
2. **Similarity Calculation**:
   - Compute cosine similarity between user vector and all job vectors
   - Rank jobs by similarity score
3. **Skill Gap Analysis**:
   - Compare user skills with required skills
   - Identify missing skills
   - Calculate gap percentage

## Technology Stack

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **CSS**: Custom styling (no heavy frameworks)

### Backend
- **FastAPI**: Modern Python web framework
- **PyPDF2**: PDF parsing
- **scikit-learn**: ML algorithms (TF-IDF, Cosine Similarity)
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **python-jose**: JWT token handling
- **Pydantic**: Data validation

### Data Storage
- **In-memory**: User authentication (can be replaced with Supabase)
- **CSV**: Job dataset (can be migrated to database)

## Security

1. **Authentication**: JWT-based token authentication
2. **Password Hashing**: SHA-256 (use bcrypt in production)
3. **CORS**: Configured for cross-origin requests
4. **File Validation**: PDF type and size validation
5. **Input Validation**: Pydantic schemas for all inputs

## Scalability Considerations

### Current (Phase 1)
- In-memory user storage
- CSV-based job dataset
- Single server deployment

### Future Enhancements
- Database integration (Supabase/PostgreSQL)
- Redis for caching
- Microservices architecture
- Containerization (Docker)
- Cloud deployment (Vercel + Render)

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Resume
- `POST /api/v1/resume/upload` - Upload and process resume
- `POST /api/v1/resume/extract-skills` - Extract skills from text

### Recommendations
- `POST /api/v1/jobs/recommend` - Get job recommendations
- `GET /api/v1/jobs/skill-gap/{job_id}` - Get skill gap analysis

## Deployment Architecture

### Local Development
- Frontend: `http://localhost:3000` (Vite dev server)
- Backend: `http://localhost:8000` (Uvicorn)

### Production (Cloud)
- Frontend: Vercel (static hosting)
- Backend: Render (Python service)
- Database: Supabase (PostgreSQL)
- File Storage: Supabase Storage (for resumes)

## Performance Optimizations

1. **TF-IDF Caching**: Pre-compute job vectors on startup
2. **Lazy Loading**: Load recommendations on demand
3. **Pagination**: Limit number of recommendations returned
4. **File Size Limits**: Restrict PDF upload size

## Error Handling

- Global exception handler in FastAPI
- Try-catch blocks in services
- User-friendly error messages
- HTTP status codes for different error types

## Future Enhancements

1. **Advanced NLP**: Use transformer models for better skill extraction
2. **User Profiles**: Store user data and resume history
3. **Job Application Tracking**: Track applied jobs
4. **Learning Paths**: Recommend courses to fill skill gaps
5. **Real-time Updates**: WebSocket for live recommendations
6. **Multi-language Support**: Support for multiple languages
