"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# ============ Auth Schemas ============
class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str


# ============ Resume Schemas ============
class ResumeUploadResponse(BaseModel):
    """Response after resume upload"""
    message: str
    resume_id: str
    extracted_text: str
    extracted_skills: List[str]


class SkillExtractionResponse(BaseModel):
    """Skill extraction response"""
    skills: List[str]
    skill_count: int


# ============ Job Recommendation Schemas ============
class JobRecommendation(BaseModel):
    """Single job recommendation"""
    job_id: str
    job_title: str
    match_score: float = Field(..., ge=0.0, le=1.0)
    match_percentage: float = Field(..., ge=0.0, le=100.0)
    required_skills: List[str]
    user_skills: List[str]
    missing_skills: List[str]
    skill_gap_count: int


class JobRecommendationResponse(BaseModel):
    """Response containing job recommendations"""
    user_skills: List[str]
    total_jobs_found: int
    recommendations: List[JobRecommendation]


# ============ Error Schemas ============
class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: Optional[str] = None






