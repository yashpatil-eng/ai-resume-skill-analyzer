"""
Database service for Supabase integration
Handles all database operations for the AI Career Intelligence Platform
"""
from app.core.config import supabase
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class DatabaseService:
    """Database service for user management and data persistence"""

    @staticmethod
    async def create_user(email: str, password_hash: str, full_name: str) -> Optional[Dict[str, Any]]:
        """Create a new user in database"""
        if not supabase:
            logger.error("Supabase client not available")
            return None

        try:
            result = supabase.table('users').insert({
                'email': email,
                'password_hash': password_hash,
                'full_name': full_name
            }).execute()

            if result.data and len(result.data) > 0:
                logger.info(f"User created successfully: {email}")
                return result.data[0]
            else:
                logger.error(f"Failed to create user: {email}")
                return None

        except Exception as e:
            logger.error(f"Error creating user {email}: {str(e)}")
            return None

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        if not supabase:
            logger.error("Supabase client not available")
            return None

        try:
            result = supabase.table('users').select('*').eq('email', email).execute()

            if result.data and len(result.data) > 0:
                return result.data[0]
            else:
                return None

        except Exception as e:
            logger.error(f"Error getting user by email {email}: {str(e)}")
            return None

    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            result = supabase.table('users').select('*').eq('user_id', user_id).execute()

            if result.data and len(result.data) > 0:
                return result.data[0]
            else:
                return None

        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {str(e)}")
            return None

    @staticmethod
    async def save_resume(user_id: str, filename: str, extracted_text: str, extracted_skills: List[str]) -> bool:
        """Save resume data to database"""
        logger.info(f"Attempting to save resume for user_id: {user_id}, filename: {filename}")

        if not supabase:
            logger.error("Supabase client not available")
            return False

        try:
            # Prepare data for insertion
            resume_data = {
                'user_id': user_id,
                'filename': filename,
                'extracted_text': extracted_text,
                'extracted_skills': extracted_skills
            }

            logger.info(f"Inserting resume data: user_id={user_id}, filename={filename}")

            result = supabase.table('resumes').insert(resume_data).execute()

            if result.data and len(result.data) > 0:
                logger.info(f"Resume saved successfully for user {user_id}: {result.data[0]}")
                return True
            else:
                logger.error(f"Failed to save resume for user {user_id}: No data returned")
                return False

        except Exception as e:
            logger.error(f"Error saving resume for user {user_id}: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            return False

    @staticmethod
    async def get_user_resumes(user_id: str) -> List[Dict[str, Any]]:
        """Get all resumes for a user"""
        try:
            result = supabase.table('resumes').select('*').eq('user_id', user_id).order('uploaded_at', desc=True).execute()

            if result.data:
                return result.data
            else:
                return []

        except Exception as e:
            logger.error(f"Error getting resumes for user {user_id}: {str(e)}")
            return []

    @staticmethod
    async def save_job_recommendation(user_id: str, user_skills: List[str], recommendations: List[Dict[str, Any]]) -> bool:
        """Save job recommendations for caching"""
        try:
            result = supabase.table('job_recommendations').insert({
                'user_id': user_id,
                'user_skills': user_skills,
                'recommendations': recommendations
            }).execute()

            if result.data and len(result.data) > 0:
                logger.info(f"Job recommendations saved for user {user_id}")
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error saving job recommendations for user {user_id}: {str(e)}")
            return False

    @staticmethod
    async def get_user_recommendations(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent job recommendations for a user"""
        try:
            result = supabase.table('job_recommendations').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()

            if result.data:
                return result.data
            else:
                return []

        except Exception as e:
            logger.error(f"Error getting recommendations for user {user_id}: {str(e)}")
            return []

    @staticmethod
    async def update_user_profile(user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user profile information"""
        try:
            result = supabase.table('users').update(updates).eq('user_id', user_id).execute()

            if result.data and len(result.data) > 0:
                logger.info(f"User profile updated: {user_id}")
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error updating user profile {user_id}: {str(e)}")
            return False

    @staticmethod
    async def delete_user_data(user_id: str) -> bool:
        """Delete all user data (GDPR compliance)"""
        try:
            # Delete in correct order due to foreign keys
            supabase.table('job_recommendations').delete().eq('user_id', user_id).execute()
            supabase.table('resumes').delete().eq('user_id', user_id).execute()
            supabase.table('user_sessions').delete().eq('user_id', user_id).execute()
            supabase.table('users').delete().eq('user_id', user_id).execute()

            logger.info(f"All data deleted for user: {user_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting user data {user_id}: {str(e)}")
            return False
