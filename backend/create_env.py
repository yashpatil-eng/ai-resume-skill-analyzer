"""
Script to create .env file for local development
Run this script to generate a .env file with default values
"""
import secrets
import os

def create_env_file():
    """Create .env file with default values"""
    
    # Generate a secure secret key
    secret_key = secrets.token_urlsafe(32)
    
    env_content = f"""# ============================================
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
# This is a generated key for local development
# IMPORTANT: Change this in production!
SECRET_KEY={secret_key}
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
"""
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    # Check if .env already exists
    if os.path.exists(env_path):
        print(".env file already exists. Overwriting...")
    
    # Write .env file
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"[OK] .env file created successfully at: {env_path}")
    print(f"[OK] Generated SECRET_KEY: {secret_key[:20]}...")
    print("\nYou can now start the server with: python -m app.main")

if __name__ == "__main__":
    create_env_file()

