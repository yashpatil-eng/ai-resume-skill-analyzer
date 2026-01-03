"""
Resume parsing service using PyPDF2
Extracts text from PDF resumes
"""
import PyPDF2
import io
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ResumeParser:
    """Service for parsing PDF resumes"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_bytes: bytes) -> str:
        """
        Extract text content from PDF file bytes
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            Extracted text as string
            
        Raises:
            ValueError: If PDF cannot be parsed
        """
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text_content = []
            
            # Extract text from all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_content.append(text)
            
            full_text = "\n".join(text_content)
            
            if not full_text.strip():
                raise ValueError("No text content found in PDF")
            
            logger.info(f"Successfully extracted {len(full_text)} characters from PDF")
            return full_text
            
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    @staticmethod
    def validate_pdf(pdf_bytes: bytes) -> bool:
        """
        Validate if the uploaded file is a valid PDF
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            PyPDF2.PdfReader(pdf_file)
            return True
        except Exception:
            return False






