#!/usr/bin/env python3
"""
Test Supabase connection and database operations
"""
import asyncio
from app.core.config import supabase
from app.services.database import DatabaseService

async def test_supabase():
    """Test Supabase connection and basic operations"""

    print("🔍 Testing Supabase Connection...")

    if not supabase:
        print("❌ Supabase client not initialized")
        return

    print("✅ Supabase client initialized")

    # Test connection by trying to select from users table
    try:
        result = supabase.table('users').select('count', count='exact').execute()
        print(f"✅ Database connection successful - found {result.count} users")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return

    # Test user creation
    print("\n🧪 Testing user creation...")
    try:
        test_email = f"test_{int(asyncio.get_event_loop().time())}@example.com"
        user = await DatabaseService.create_user(test_email, "test_hash", "Test User")
        if user:
            print(f"✅ User created successfully: {user['email']}")

            # Clean up test user
            try:
                supabase.table('users').delete().eq('email', test_email).execute()
                print("✅ Test user cleaned up")
            except Exception as e:
                print(f"⚠️  Could not clean up test user: {e}")
        else:
            print("❌ User creation failed")
    except Exception as e:
        print(f"❌ User creation test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_supabase())



