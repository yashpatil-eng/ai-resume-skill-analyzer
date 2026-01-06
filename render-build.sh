#!/usr/bin/env bash

# Render-specific build script
# Render runs this from the backend directory and expects production-ready deployment

set -e

echo "🎨 Starting Render deployment build..."

# Render provides Python environment, but let's verify
python --version

# Set environment variables for Render
export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1

# Update pip and tools
pip install --upgrade pip setuptools wheel

# Force binary installation of ML libraries (critical for Render)
echo "🤖 Installing ML libraries from pre-built wheels..."
pip install --only-binary=all --force-reinstall \
    numpy==1.26.4 \
    pandas==2.2.3 \
    scipy==1.14.1 \
    scikit-learn==1.5.2 \
    joblib==1.4.2 \
    threadpoolctl==3.5.0

# Verify ML libraries work
python -c "
import numpy, pandas, sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
print('✅ ML libraries ready')
"

# Install all dependencies
pip install -r requirements.txt

# Verify all imports
python -c "
import fastapi, uvicorn, pydantic, supabase, PyPDF2
from jose import jwt
print('✅ All dependencies verified')
"

echo "✅ Render build completed successfully!"

