"""
Job recommendation service using TF-IDF and Cosine Similarity
Recommends jobs based on user skills extracted from resume
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import logging
import os

logger = logging.getLogger(__name__)


class JobRecommender:
    """Service for recommending jobs based on user skills"""
    
    def __init__(self, dataset_path: str = "dataset/jobs.csv"):
        """
        Initialize job recommender with dataset
        
        Args:
            dataset_path: Path to jobs CSV file
        """
        self.dataset_path = dataset_path
        self.jobs_df = None
        self.vectorizer = None
        self.job_vectors = None
        self._load_dataset()
        self._initialize_vectorizer()
    
    def _load_dataset(self):
        """Load jobs dataset from CSV"""
        try:
            # Get the project root directory (parent of backend)
            current_file = os.path.abspath(__file__)
            services_dir = os.path.dirname(current_file)
            app_dir = os.path.dirname(services_dir)
            backend_dir = os.path.dirname(app_dir)
            project_root = os.path.dirname(backend_dir)
            
            # Try multiple paths
            possible_paths = [
                self.dataset_path,  # Relative from current working directory
                os.path.join(project_root, self.dataset_path),  # From project root
                os.path.join(os.getcwd(), self.dataset_path),  # From current working directory
                os.path.join(backend_dir, "..", self.dataset_path),  # Relative from backend
            ]
            
            dataset_found = False
            for path in possible_paths:
                abs_path = os.path.abspath(path)
                if os.path.exists(abs_path):
                    self.jobs_df = pd.read_csv(abs_path)
                    dataset_found = True
                    logger.info(f"Loaded dataset from: {abs_path}")
                    break
            
            if not dataset_found:
                raise FileNotFoundError(
                    f"Jobs dataset not found. Tried paths: {possible_paths}. "
                    f"Please ensure dataset/jobs.csv exists in the project root."
                )
            
            # Validate required columns
            required_cols = ["job_id", "job_title", "skills"]
            missing_cols = [col for col in required_cols if col not in self.jobs_df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            logger.info(f"Loaded {len(self.jobs_df)} jobs from dataset")
            
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise
    
    def _initialize_vectorizer(self):
        """Initialize TF-IDF vectorizer and create job vectors"""
        try:
            # Combine job title and skills for better matching
            self.jobs_df["combined_text"] = (
                self.jobs_df["job_title"].astype(str) + " " + 
                self.jobs_df["skills"].astype(str)
            )
            
            # Initialize TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words='english',
                ngram_range=(1, 2),  # Unigrams and bigrams
                min_df=1,
                max_features=1000
            )
            
            # Fit and transform job descriptions
            self.job_vectors = self.vectorizer.fit_transform(
                self.jobs_df["combined_text"].tolist()
            )
            
            logger.info("TF-IDF vectorizer initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing vectorizer: {str(e)}")
            raise
    
    def recommend_jobs(
        self, 
        user_skills: List[str], 
        top_n: int = 10,
        min_similarity: float = 0.1
    ) -> List[Dict]:
        """
        Recommend jobs based on user skills
        
        Args:
            user_skills: List of user's skills
            top_n: Number of top recommendations to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of job recommendations with match scores
        """
        if not user_skills:
            logger.warning("No user skills provided for recommendation")
            return []
        
        try:
            # Convert user skills to text
            user_skills_text = " ".join(user_skills).lower()
            
            # Transform user skills to TF-IDF vector
            user_vector = self.vectorizer.transform([user_skills_text])
            
            # Calculate cosine similarity
            similarities = cosine_similarity(user_vector, self.job_vectors)[0]
            
            # Get top N recommendations
            top_indices = np.argsort(similarities)[::-1][:top_n]
            
            recommendations = []
            
            for idx in top_indices:
                similarity_score = float(similarities[idx])
                
                # Filter by minimum similarity
                if similarity_score < min_similarity:
                    continue
                
                job_row = self.jobs_df.iloc[idx]
                job_id = str(job_row["job_id"])
                job_title = str(job_row["job_title"])
                required_skills_str = str(job_row["skills"])
                
                # Parse required skills (space-separated within quoted CSV field)
                required_skills = [
                    s.strip().lower()
                    for s in required_skills_str.split()
                    if s.strip()
                ]
                
                # Calculate skill gap
                user_skills_lower = [s.lower() for s in user_skills]
                missing_skills = [
                    skill for skill in required_skills 
                    if skill not in user_skills_lower
                ]
                
                recommendation = {
                    "job_id": job_id,
                    "job_title": job_title,
                    "match_score": similarity_score,
                    "match_percentage": round(similarity_score * 100, 2),
                    "required_skills": required_skills,
                    "user_skills": user_skills,
                    "missing_skills": missing_skills,
                    "skill_gap_count": len(missing_skills)
                }
                
                recommendations.append(recommendation)
            
            # Sort by match score (descending)
            recommendations.sort(key=lambda x: x["match_score"], reverse=True)
            
            logger.info(f"Generated {len(recommendations)} job recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            raise ValueError(f"Failed to generate recommendations: {str(e)}")
    
    def get_skill_gap_analysis(
        self, 
        user_skills: List[str], 
        job_id: str
    ) -> Dict:
        """
        Get detailed skill gap analysis for a specific job
        
        Args:
            user_skills: List of user's skills
            job_id: Target job ID
            
        Returns:
            Dictionary with skill gap analysis
        """
        try:
            job_row = self.jobs_df[self.jobs_df["job_id"] == job_id]
            
            if job_row.empty:
                raise ValueError(f"Job with ID {job_id} not found")
            
            required_skills_str = str(job_row.iloc[0]["skills"])
            required_skills = [
                s.strip().lower()
                for s in required_skills_str.split()
                if s.strip()
            ]
            
            user_skills_lower = [s.lower() for s in user_skills]
            
            matching_skills = [
                skill for skill in required_skills 
                if skill in user_skills_lower
            ]
            
            missing_skills = [
                skill for skill in required_skills 
                if skill not in user_skills_lower
            ]
            
            return {
                "required_skills": required_skills,
                "user_skills": user_skills,
                "matching_skills": matching_skills,
                "missing_skills": missing_skills,
                "match_percentage": round(
                    len(matching_skills) / len(required_skills) * 100, 2
                ) if required_skills else 0.0,
                "skill_gap_count": len(missing_skills)
            }
            
        except Exception as e:
            logger.error(f"Error in skill gap analysis: {str(e)}")
            raise

