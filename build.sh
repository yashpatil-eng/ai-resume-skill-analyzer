#!/usr/bin/env bash

# Build script for Render deployment - Python 3.12.7 optimized
# Forces binary installation and handles Python version conflicts

set -e

echo "🚀 Starting AI Career Intelligence Platform build on Render..."
echo "🐍 Target Python version: 3.12.7"

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "📊 Current Python version: $python_version"

# Force pip to use compatible versions
export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1

# Update pip and install build tools
echo "📦 Updating pip and build tools..."
pip install --upgrade pip setuptools wheel

# Force binary installation of ML libraries (critical for Render Python 3.12.7)
echo "🤖 Installing ML libraries from pre-built wheels..."
pip install --only-binary=all --force-reinstall \
    numpy==1.26.4 \
    pandas==2.1.4 \
    scipy==1.11.4 \
    scikit-learn==1.3.2 \
    joblib==1.3.2 \
    threadpoolctl==3.2.0

# Verify ML libraries installed correctly
echo "🔍 Verifying ML library installation..."
python -c "
import sys
print(f'Python version: {sys.version}')
import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
print(f'✅ NumPy: {np.__version__}')
print(f'✅ Pandas: {pd.__version__}')
print(f'✅ Scikit-learn: {sklearn.__version__}')
print('✅ ML libraries installed successfully')
"

# Install remaining dependencies
echo "📚 Installing remaining dependencies..."
pip install -r requirements.txt

# Verify all critical imports work
echo "🧪 Testing all critical imports..."
python -c "
# Core FastAPI
import fastapi
import uvicorn
import pydantic
import pydantic_settings

# Authentication
from python_jose import jwt
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
print('🎉 Build verification complete!')
"

echo "🎉 Build completed successfully!"
echo "🚀 Your AI Career Intelligence Platform is ready for deployment on Python 3.12.7!"
