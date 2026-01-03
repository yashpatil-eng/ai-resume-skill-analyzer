"""
Job recommendation routes
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
import logging

from app.models.schemas import JobRecommendationResponse, JobRecommendation
from app.services.recommender import JobRecommender
from app.routes.auth import get_current_user
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter(prefix="/jobs", tags=["Job Recommendations"])

# Initialize recommender
try:
    recommender = JobRecommender(dataset_path=settings.DATASET_PATH)
except Exception as e:
    logging.error(f"Failed to initialize recommender: {str(e)}")
    recommender = None

logger = logging.getLogger(__name__)


class JobRecommendationRequest(BaseModel):
    """Request model for job recommendations"""
    user_skills: List[str]
    top_n: int = 10


@router.post("/recommend", response_model=JobRecommendationResponse)
async def recommend_jobs(
    request: JobRecommendationRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Get job recommendations based on user skills
    
    Args:
        request: JobRecommendationRequest with user_skills and top_n
        
    Returns:
        Job recommendations with match scores and skill gaps
    """
    if not recommender:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Recommendation service is not available"
        )
    
    if not request.user_skills:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User skills are required"
        )
    
    try:
        # Get job recommendations
        recommendations_data = recommender.recommend_jobs(
            user_skills=request.user_skills,
            top_n=request.top_n,
            min_similarity=settings.MIN_SIMILARITY_THRESHOLD
        )
        
        # Convert to response models
        recommendations = [
            JobRecommendation(**rec) for rec in recommendations_data
        ]
        
        # Save recommendations to database for caching
        from app.services.database import DatabaseService
        save_success = await DatabaseService.save_job_recommendation(
            current_user['user_id'],
            request.user_skills,
            recommendations_data  # Save the raw data
        )

        if not save_success:
            logger.warning(f"Failed to save job recommendations to database for user {current_user['user_id']}")

        logger.info(
            f"Generated {len(recommendations)} recommendations for user {current_user['user_id']}"
        )

        return JobRecommendationResponse(
            user_skills=request.user_skills,
            total_jobs_found=len(recommendations),
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


class SkillGapRequest(BaseModel):
    """Request model for skill gap analysis"""
    user_skills: List[str]


@router.post("/skill-gap/{job_id}")
async def get_skill_gap(
    job_id: str,
    request: SkillGapRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed skill gap analysis for a specific job
    
    Args:
        job_id: Target job ID
        user_skills: List of user's skills
        
    Returns:
        Detailed skill gap analysis
    """
    if not recommender:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Recommendation service is not available"
        )
    
    try:
        skill_gap = recommender.get_skill_gap_analysis(
            user_skills=request.user_skills,
            job_id=job_id
        )
        
        return skill_gap
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in skill gap analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in skill gap analysis: {str(e)}"
        )

