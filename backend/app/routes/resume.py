"""
Resume upload and processing routes
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, Query
from fastapi.responses import JSONResponse
import uuid
import logging

from app.models.schemas import ResumeUploadResponse, SkillExtractionResponse
from app.services.resume_parser import ResumeParser
from app.services.skill_extractor import SkillExtractor
from app.services.database import DatabaseService
from app.routes.auth import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/resume", tags=["Resume"])

# Initialize services
resume_parser = ResumeParser()
skill_extractor = SkillExtractor()

logger = logging.getLogger(__name__)


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload and process resume PDF

    Extracts text and skills from uploaded PDF resume
    """
    logger.info("DEBUG: upload_resume function called")
    logger.info(f"DEBUG: File: {file.filename}")
    logger.info(f"DEBUG: Current user: {current_user}")

    # Read file content
    file_content = await file.read()
    logger.info(f"DEBUG: File size: {len(file_content)} bytes")

    # Validate file type
    if not file.filename.endswith(".pdf"):
        print("DEBUG: File type validation failed")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    try:
        # file_content already read above
        
        # Validate file size
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB"
            )
        
        # Validate PDF
        if not resume_parser.validate_pdf(file_content):
            raise ValueError("Invalid PDF file")
        
        # Extract text from PDF
        extracted_text = resume_parser.extract_text_from_pdf(file_content)
        
        # Extract skills from text
        extracted_skills = skill_extractor.extract_skills(extracted_text)
        
        # Generate resume ID
        resume_id = str(uuid.uuid4())
        
        # Debug: Log current user info
        print(f"DEBUG: Current user object: {current_user}")
        print(f"DEBUG: Current user type: {type(current_user)}")
        print(f"DEBUG: User ID: {current_user.get('user_id', 'NOT FOUND')}")
        print(f"DEBUG: User email: {current_user.get('email', 'NOT FOUND')}")

        # Ensure user_id exists
        if 'user_id' not in current_user:
            raise ValueError(f"User object missing user_id: {current_user}")

        # Save resume to database
        save_success = DatabaseService.save_resume(
            current_user['user_id'],
            file.filename,
            extracted_text,
            extracted_skills
        )

        if not save_success:
            logger.warning(f"Failed to save resume to database for user {current_user['user_id']}")
        else:
            logger.info(f"Successfully saved resume for user {current_user['user_id']}")

        logger.info(
            f"Resume processed for user {current_user['user_id']}: "
            f"{len(extracted_skills)} skills extracted"
        )

        return ResumeUploadResponse(
            message="Resume processed successfully",
            resume_id=resume_id,
            extracted_text=extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            extracted_skills=extracted_skills
        )
        
    except ValueError as e:
        print(f"DEBUG: ValueError caught: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        print("DEBUG: HTTPException re-raised")
        raise  # Re-raise HTTPException to be handled by FastAPI
    except Exception as e:
        error_msg = str(e) if str(e) else f"Unknown error: {type(e).__name__}"
        print(f"DEBUG: General exception: {error_msg}, type: {type(e)}")
        logger.error(f"Error processing resume: {error_msg}")
        logger.error(f"Full exception: {repr(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {error_msg}"
        )


@router.post("/extract-skills", response_model=SkillExtractionResponse)
async def extract_skills_from_text(
    text: str = Query(..., description="Text content to extract skills from"),
    current_user: dict = Depends(get_current_user)
):
    """
    Extract skills from provided text
    
    Useful for testing or extracting skills from text input
    Accepts text as query parameter: ?text=your_text_here
    """
    if not text or not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text input is required and cannot be empty"
        )
    
    try:
        skills = skill_extractor.extract_skills(text)
        
        return SkillExtractionResponse(
            skills=skills,
            skill_count=len(skills)
        )
        
    except Exception as e:
        logger.error(f"Error extracting skills: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting skills: {str(e)}"
        )

