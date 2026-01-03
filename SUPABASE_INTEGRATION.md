# Supabase Database Integration Guide

## 🚀 Step-by-Step Supabase Integration

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login to your account
3. Click "New Project"
4. Fill in project details:
   - **Name**: `ai-career-platform`
   - **Database Password**: Choose a strong password
   - **Region**: Select closest to your location
5. Click "Create new project"

### Step 2: Get API Keys

1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy the following values:
   - **Project URL**: `https://your-project-id.supabase.co`
   - **anon/public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - **service_role key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### Step 3: Update Environment Variables

Update your `backend/.env` file:

```env
# Database Settings
DATABASE_URL=postgresql://postgres:[password]@db.your-project-id.supabase.co:5432/postgres
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_ANON_KEY=your-anon-public-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Step 4: Install Supabase Python Client

```bash
cd backend
pip install supabase
```

### Step 5: Create Database Tables

Run this SQL in your Supabase SQL Editor:

```sql
-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Resumes table
CREATE TABLE resumes (
    resume_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    filename VARCHAR(255),
    extracted_text TEXT,
    extracted_skills JSONB,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Job recommendations table (optional - for caching)
CREATE TABLE job_recommendations (
    recommendation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    user_skills JSONB,
    recommendations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_recommendations ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own data" ON users
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view own resumes" ON resumes
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view own recommendations" ON job_recommendations
    FOR ALL USING (auth.uid() = user_id);
```

### Step 6: Update Backend Configuration

Update `backend/app/core/config.py`:

```python
# Add these imports at the top
from supabase import create_client, Client

# Add database client initialization
class Settings(BaseSettings):
    # ... existing settings ...

    # Supabase client property
    @property
    def supabase_client(self) -> Client:
        return create_client(self.SUPABASE_URL, self.SUPABASE_KEY)

# Create global supabase client
settings = Settings()
supabase: Client = settings.supabase_client
```

### Step 7: Update Authentication Service

Create `backend/app/services/database.py`:

```python
from app.core.config import supabase
from typing import Optional, Dict, Any

class DatabaseService:
    """Database service for user management"""

    @staticmethod
    async def create_user(email: str, password_hash: str, full_name: str) -> Optional[Dict[str, Any]]:
        """Create a new user in database"""
        try:
            result = supabase.table('users').insert({
                'email': email,
                'password_hash': password_hash,
                'full_name': full_name
            }).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            result = supabase.table('users').select('*').eq('email', email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    @staticmethod
    async def save_resume(user_id: str, filename: str, extracted_text: str, extracted_skills: list) -> bool:
        """Save resume data"""
        try:
            supabase.table('resumes').insert({
                'user_id': user_id,
                'filename': filename,
                'extracted_text': extracted_text,
                'extracted_skills': extracted_skills
            }).execute()
            return True
        except Exception as e:
            print(f"Error saving resume: {e}")
            return False
```

### Step 8: Update Auth Routes

Update `backend/app/routes/auth.py`:

```python
# Replace the in-memory users_db with database calls
from app.services.database import DatabaseService

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """Register a new user"""

    # Check if user already exists
    existing_user = await DatabaseService.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    password_hash = hash_password(user_data.password)
    user = await DatabaseService.create_user(
        user_data.email,
        password_hash,
        user_data.full_name
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email, "user_id": str(user['user_id'])},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user['user_id']),
        email=user_data.email
    )

@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin):
    """Login user and return JWT token"""

    # Get user from database
    user = await DatabaseService.get_user_by_email(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password
    if not verify_password(user_credentials.password, user['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email'], "user_id": str(user['user_id'])},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user['user_id']),
        email=user['email']
    )
```

### Step 9: Update Resume Routes

Update `backend/app/routes/resume.py`:

```python
from app.services.database import DatabaseService

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # ... existing code ...

    # Save to database
    success = await DatabaseService.save_resume(
        current_user['user_id'],
        file.filename,
        extracted_text,
        extracted_skills
    )

    if not success:
        # Still return success but log the database error
        logger.warning(f"Failed to save resume to database for user {current_user['user_id']}")

    return ResumeUploadResponse(
        message="Resume processed successfully",
        resume_id=resume_id,
        extracted_text=extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
        extracted_skills=extracted_skills
    )
```

### Step 10: Update Requirements

Add to `backend/requirements.txt`:

```txt
# Supabase
supabase==2.3.0
```

### Step 11: Enable Supabase Auth (Optional)

For production authentication, you can use Supabase Auth:

1. In Supabase Dashboard → Authentication → Settings
2. Configure auth providers (optional)
3. Update frontend to use Supabase Auth instead of custom JWT

### Step 12: Test the Integration

1. Restart your backend server
2. Test registration/login - data should be saved to Supabase
3. Upload resumes - data should be saved to Supabase
4. Check your Supabase dashboard to verify data is being stored

### Step 13: Environment Variables for Production

For production deployment:

```env
# Production Supabase settings
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-production-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-production-service-role-key
DATABASE_URL=postgresql://postgres:[password]@db.your-project-id.supabase.co:5432/postgres
```

## 🔧 Troubleshooting

### Connection Issues
- Check your Supabase project is active
- Verify API keys are correct
- Check firewall settings

### Authentication Issues
- Ensure RLS policies are correctly set
- Check user permissions
- Verify JWT token format

### Data Not Saving
- Check table schemas
- Verify foreign key relationships
- Check Supabase logs

## 📊 Supabase Features You Get

- ✅ **Real-time subscriptions**
- ✅ **Row Level Security (RLS)**
- ✅ **Built-in authentication**
- ✅ **File storage** (for resume files)
- ✅ **Real-time database**
- ✅ **Automatic API generation**
- ✅ **Serverless functions**

## 🚀 Next Steps

1. **File Storage**: Store actual PDF files in Supabase Storage
2. **Real-time Updates**: Add real-time job recommendations
3. **Advanced Analytics**: Track user behavior
4. **Admin Dashboard**: Manage users and content
5. **Backup**: Automated database backups

---

**Your AI Career Intelligence Platform is now database-ready! 🎉**



