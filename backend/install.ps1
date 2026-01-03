# Windows Installation Script for AI Career Intelligence Platform
# Run this script from the backend directory

Write-Host "Installing dependencies for Windows..." -ForegroundColor Green

# Upgrade pip, setuptools, and wheel first
Write-Host "Upgrading pip, setuptools, and wheel..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# Install core dependencies first
Write-Host "Installing core dependencies..." -ForegroundColor Yellow
pip install fastapi==0.104.1
pip install "uvicorn[standard]==0.24.0"
pip install python-multipart==0.0.6
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0

# Install authentication dependencies
Write-Host "Installing authentication dependencies..." -ForegroundColor Yellow
pip install "python-jose[cryptography]==3.3.0"
pip install "passlib[bcrypt]==1.7.4"

# Install PDF processing
Write-Host "Installing PDF processing..." -ForegroundColor Yellow
pip install PyPDF2==3.0.1

# Install ML dependencies - try with wheel-only first
Write-Host "Installing ML dependencies (this may take a while)..." -ForegroundColor Yellow
Write-Host "Installing numpy..." -ForegroundColor Cyan
pip install numpy==1.24.3

Write-Host "Installing pandas..." -ForegroundColor Cyan
pip install pandas==2.0.3

Write-Host "Installing scikit-learn (using pre-built wheels only)..." -ForegroundColor Cyan
pip install scikit-learn==1.3.1 --only-binary :all:

# If the above fails, try without version pinning
if ($LASTEXITCODE -ne 0) {
    Write-Host "Retrying scikit-learn installation with latest compatible version..." -ForegroundColor Yellow
    pip install scikit-learn --only-binary :all:
}

Write-Host "`nInstallation complete!" -ForegroundColor Green
Write-Host "Verify installation by running: python -c 'import fastapi, sklearn, pandas; print(\"All OK!\")'" -ForegroundColor Cyan






