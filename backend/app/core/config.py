"""
Configuration settings for the AI Career Intelligence Platform
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AI Career Intelligence Platform"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database (Supabase/PostgreSQL)
    DATABASE_URL: Optional[str] = None
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf"]
    UPLOAD_DIR: str = "uploads"
    
    # ML/NLP Settings
    DATASET_PATH: str = "dataset/jobs.csv"
    MIN_SIMILARITY_THRESHOLD: float = 0.1

    # CORS Settings
    CORS_ORIGINS_STR: Optional[str] = None

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"  # Ignore extra fields from .env file
    }

    @property
    def CORS_ORIGINS(self):
        """Parse CORS origins from string"""
        if self.CORS_ORIGINS_STR:
            return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(",")]
        return []

    # Supabase client property
    @property
    def supabase_client(self):
        """Get Supabase client instance"""
        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            print("Warning: SUPABASE_URL or SUPABASE_KEY not set in .env file")
            return None

        try:
            from supabase import create_client
            # Create client without auth features that might cause issues
            return create_client(self.SUPABASE_URL, self.SUPABASE_KEY)
        except ImportError:
            print("Warning: supabase package not installed. Install with: pip install supabase")
            return None
        except Exception as e:
            print(f"Warning: Could not initialize Supabase client: {e}")
            print("Falling back to database-less mode")
            return None


settings = Settings()

# Initialize Supabase client
try:
    supabase = settings.supabase_client
    if supabase:
        print("Supabase client initialized successfully")
    else:
        print("Supabase client not initialized - check your credentials")
        supabase = None
except Exception as e:
    print(f"Error initializing Supabase client: {e}")
    supabase = None

