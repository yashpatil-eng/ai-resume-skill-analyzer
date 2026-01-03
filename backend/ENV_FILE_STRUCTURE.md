# .env File Structure

## Quick Setup

Run this command to create the `.env` file:

```powershell
cd backend
python create_env.py
```

Or manually create a file named `.env` in the `backend/` directory with the following content:

## .env File Content

```env
# ============================================
# AI Career Intelligence Platform - Environment Variables
# ============================================
# Local Development Configuration
# DO NOT commit this file to version control!

# ============================================
# API Settings
# ============================================
API_V1_PREFIX=/api/v1
PROJECT_NAME=AI Career Intelligence Platform
VERSION=1.0.0

# ============================================
# Security Settings
# ============================================
# Secret key for JWT token signing
# Generate a new one using: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=sVBFfzXrpb7jcSle7ulphiDIhXzhjwA73p25Fw3fl-o
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# Database Settings (Optional - for future Supabase integration)
# ============================================
# Uncomment and fill these when integrating with Supabase/PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-supabase-anon-key

# ============================================
# File Upload Settings
# ============================================
# Maximum file size in bytes (10MB = 10485760 bytes)
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=uploads

# ============================================
# ML/NLP Settings
# ============================================
# Path to jobs dataset (relative to project root)
DATASET_PATH=dataset/jobs.csv
# Minimum similarity threshold for job recommendations (0.0 to 1.0)
# Lower values = more recommendations, Higher values = fewer but more relevant
MIN_SIMILARITY_THRESHOLD=0.1
```

## File Location

Create the `.env` file in: `backend/.env`

## Environment Variables Explained

### API Settings
- `API_V1_PREFIX`: The URL prefix for all API routes (default: `/api/v1`)
- `PROJECT_NAME`: Name of the application
- `VERSION`: Application version

### Security Settings
- `SECRET_KEY`: **REQUIRED** - Secret key for JWT token signing. Must be changed in production!
- `ALGORITHM`: JWT signing algorithm (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes (default: `30`)

### Database Settings (Optional)
- `DATABASE_URL`: PostgreSQL connection string (for future use)
- `SUPABASE_URL`: Supabase project URL (for future use)
- `SUPABASE_KEY`: Supabase API key (for future use)

### File Upload Settings
- `MAX_UPLOAD_SIZE`: Maximum file upload size in bytes (default: `10485760` = 10MB)
- `UPLOAD_DIR`: Directory where uploaded files are stored (default: `uploads`)

### ML/NLP Settings
- `DATASET_PATH`: Path to the jobs CSV file (relative to project root)
- `MIN_SIMILARITY_THRESHOLD`: Minimum similarity score (0.0-1.0) for job recommendations

## Generate New Secret Key

For production, generate a secure secret key:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Important Notes

1. ✅ The `.env` file is already in `.gitignore` - it won't be committed
2. ✅ Use `env.example` as a template for team members
3. ✅ Never share your `SECRET_KEY` publicly
4. ✅ Use different keys for development and production
5. ✅ The `.env` file is loaded automatically by `pydantic-settings`

## Verification

After creating the `.env` file, verify it's being read:

```python
from app.core.config import settings
print(f"Secret Key: {settings.SECRET_KEY[:20]}...")
print(f"Dataset Path: {settings.DATASET_PATH}")
```






