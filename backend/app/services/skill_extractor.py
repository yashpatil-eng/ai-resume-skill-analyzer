"""
Skill extraction service using NLP and keyword matching
Extracts technical and soft skills from resume text
"""
import re
from typing import List, Set
import logging

logger = logging.getLogger(__name__)


class SkillExtractor:
    """Service for extracting skills from resume text"""
    
    # Comprehensive skill dictionary
    TECHNICAL_SKILLS = {
        # Programming Languages
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
        "php", "ruby", "swift", "kotlin", "scala", "r", "matlab", "perl",
        
        # Web Technologies
        "html", "css", "react", "angular", "vue", "node.js", "express", "django",
        "flask", "fastapi", "spring", "laravel", "asp.net", "next.js", "nuxt.js",
        
        # Databases
        "sql", "mysql", "postgresql", "mongodb", "redis", "oracle", "sqlite",
        "cassandra", "elasticsearch", "dynamodb", "firebase",
        
        # Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git",
        "ci/cd", "terraform", "ansible", "linux", "bash", "shell scripting",
        
        # Data Science & ML
        "machine learning", "deep learning", "neural networks", "tensorflow",
        "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn",
        "data analysis", "data visualization", "nlp", "computer vision",
        "opencv", "nltk", "spacy", "jupyter", "tableau", "power bi",
        
        # Mobile Development
        "android", "ios", "react native", "flutter", "xamarin", "ionic",
        
        # Other Technologies
        "rest api", "graphql", "microservices", "agile", "scrum", "git",
        "jira", "confluence", "api development", "web services",
    }
    
    SOFT_SKILLS = {
        "leadership", "communication", "teamwork", "problem solving",
        "critical thinking", "time management", "project management",
        "collaboration", "adaptability", "creativity", "analytical thinking",
        "presentation skills", "negotiation", "mentoring", "agile methodology",
    }
    
    def __init__(self):
        """Initialize skill extractor with combined skill dictionary"""
        self.all_skills = self.TECHNICAL_SKILLS.union(self.SOFT_SKILLS)
    
    def extract_skills(self, resume_text: str) -> List[str]:
        """
        Extract skills from resume text using keyword matching
        
        Args:
            resume_text: Text content from resume
            
        Returns:
            List of extracted skills (unique, sorted)
        """
        if not resume_text:
            return []
        
        # Normalize text to lowercase
        text_lower = resume_text.lower()
        
        # Remove special characters but keep spaces
        text_clean = re.sub(r'[^\w\s]', ' ', text_lower)
        
        # Find matching skills
        found_skills = set()
        
        # Check for exact matches and variations
        for skill in self.all_skills:
            # Create pattern to match skill (word boundaries)
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_clean):
                found_skills.add(skill)
        
        # Also check for common variations
        skill_variations = {
            "js": "javascript",
            "ts": "typescript",
            "ml": "machine learning",
            "dl": "deep learning",
            "ai": "machine learning",
            "db": "database",
            "api": "rest api",
        }
        
        for abbrev, full_skill in skill_variations.items():
            if abbrev in text_clean and full_skill in self.all_skills:
                found_skills.add(full_skill)
        
        # Sort skills for consistency
        sorted_skills = sorted(list(found_skills))
        
        logger.info(f"Extracted {len(sorted_skills)} skills from resume")
        return sorted_skills
    
    def get_skill_categories(self, skills: List[str]) -> dict:
        """
        Categorize extracted skills into technical and soft skills
        
        Args:
            skills: List of extracted skills
            
        Returns:
            Dictionary with 'technical' and 'soft' skill lists
        """
        technical = [s for s in skills if s in self.TECHNICAL_SKILLS]
        soft = [s for s in skills if s in self.SOFT_SKILLS]
        
        return {
            "technical": technical,
            "soft": soft,
            "total": len(skills)
        }






