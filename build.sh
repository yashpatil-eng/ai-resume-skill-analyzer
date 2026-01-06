#!/usr/bin/env bash

# Build script for Railway deployment - optimized for Railway's build environment
# This script handles both backend and frontend builds

set -e

echo "🚀 Starting AI Career Intelligence Platform build on Railway..."

# Set environment variables for better performance
export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PYTHONUNBUFFERED=1

# Change to backend directory
cd backend

echo "🐍 Setting up Python environment..."
python --version

# Upgrade pip and install build tools
echo "📦 Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

# Install ML libraries first (most likely to fail)
echo "🤖 Installing ML libraries..."
pip install --only-binary=all --force-reinstall \
    numpy==1.26.4 \
    pandas==2.2.3 \
    scipy==1.14.1 \
    scikit-learn==1.5.2 \
    joblib==1.4.2 \
    threadpoolctl==3.5.0

# Verify ML libraries
echo "🔍 Verifying ML libraries..."
python -c "
import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
print(f'✅ NumPy: {np.__version__}')
print(f'✅ Pandas: {pd.__version__}')
print(f'✅ Scikit-learn: {sklearn.__version__}')
"

# Install remaining dependencies
echo "📚 Installing remaining dependencies..."
pip install -r requirements.txt

# Verify all critical imports
echo "🧪 Testing critical imports..."
python -c "
# Core FastAPI
import fastapi, uvicorn, pydantic, pydantic_settings

# Authentication
from jose import jwt
import passlib.hash

# PDF processing
import PyPDF2

# ML/AI functionality
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Database
import supabase

# Email validation
import email_validator

print('✅ All critical imports successful!')
"

# Go back to root directory
cd ..

echo "🎉 Backend build completed successfully!"
echo "🚀 Your AI Career Intelligence Platform backend is ready for Railway deployment!"