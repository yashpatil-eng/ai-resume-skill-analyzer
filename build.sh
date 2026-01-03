#!/usr/bin/env bash

# Build script for Render deployment
# Forces binary installation of problematic packages

set -e

echo "🚀 Starting AI Career Intelligence Platform build on Render..."

# Update pip and install build tools
echo "📦 Updating pip and build tools..."
pip install --upgrade pip setuptools wheel

# Force binary installation of ML libraries (most critical for Render)
echo "🤖 Installing ML libraries from pre-built wheels..."
pip install --only-binary=all \
    numpy==1.26.4 \
    pandas==2.1.4 \
    scipy==1.11.4 \
    scikit-learn==1.3.2 \
    joblib==1.3.2 \
    threadpoolctl==3.2.0

# Verify ML libraries installed correctly
echo "🔍 Verifying ML library installation..."
python -c "import numpy, pandas, sklearn; print('✅ ML libraries installed successfully')"

# Install remaining dependencies
echo "📚 Installing remaining dependencies..."
pip install -r requirements.txt

# Verify all imports work
echo "🧪 Testing imports..."
python -c "
import fastapi
import uvicorn
import pydantic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import supabase
import PyPDF2
print('✅ All critical imports successful!')
"

echo "🎉 Build completed successfully!"
echo "🚀 Your AI Career Intelligence Platform is ready for deployment!"
