#!/usr/bin/env python3
"""
Environment setup script for AI Career Intelligence Platform
This script helps create the necessary .env file for development
"""

import os
import sys

def create_env_file():
    """Create .env file with default development settings"""

    env_content = """# Supabase Configuration
# Replace these with your actual Supabase project credentials
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Security - Generate a secure key for production
SECRET_KEY=dev-secret-key-change-in-production

# CORS Origins (allow frontend development servers)
CORS_ORIGINS_STR=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173

# Environment
ENVIRONMENT=development

# Optional: Service role key for admin operations
# SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
"""

    env_path = os.path.join(os.path.dirname(__file__), '.env')

    try:
        with open(env_path, 'w') as f:
            f.write(env_content.strip())

        print("[SUCCESS] Created .env file successfully!")
        print(f"Location: {env_path}")
        print("\n[IMPORTANT] Update the Supabase credentials in the .env file!")
        print("   1. Go to https://supabase.com/dashboard")
        print("   2. Select your project")
        print("   3. Go to Settings > API")
        print("   4. Copy the Project URL and anon/public key")
        print("   5. Replace the placeholder values in .env")

    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

    return True

def test_configuration():
    """Test if the configuration is working"""
    print("\nTesting configuration...")

    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(__file__))

        from app.core.config import settings, supabase

        print(f"[OK] Settings loaded: SECRET_KEY={'YES' if settings.SECRET_KEY else 'NO'}")
        print(f"[OK] CORS Origins: {getattr(settings, 'CORS_ORIGINS', 'not set')}")
        print(f"[OK] Supabase client: {'YES' if supabase else 'NO'}")

        if supabase:
            print("[OK] Database connection ready!")
        else:
            print("[WARNING] Supabase not configured - update .env file with your credentials")

    except Exception as e:
        print(f"[ERROR] Configuration test failed: {e}")
        return False

    return True

if __name__ == "__main__":
    print("AI Career Intelligence Platform - Environment Setup")
    print("=" * 60)

    # Create .env file
    if create_env_file():
        # Test configuration
        test_configuration()

        print("\nSetup complete!")
        print("Next steps:")
        print("   1. Update Supabase credentials in .env")
        print("   2. Run the database setup SQL scripts")
        print("   3. Start the backend: python -m uvicorn app.main:app --reload")
        print("   4. Start the frontend: cd ../frontend && npm run dev")
