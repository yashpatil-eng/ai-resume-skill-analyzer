# Quick Fix for Windows Installation Issue

## The Problem
scikit-learn is trying to build from source, which requires Microsoft Visual C++ Build Tools.

## The Solution (Choose One)

### Option 1: Install with Pre-built Wheels Only (RECOMMENDED)

```powershell
# In your backend directory with venv activated
cd backend
venv\Scripts\activate

# Upgrade pip first
python -m pip install --upgrade pip

# Install everything EXCEPT scikit-learn first
pip install fastapi==0.104.1 "uvicorn[standard]==0.24.0" python-multipart==0.0.6
pip install pydantic==2.5.0 pydantic-settings==2.1.0
pip install "python-jose[cryptography]==3.3.0" "passlib[bcrypt]==1.7.4"
pip install PyPDF2==3.0.1
pip install numpy pandas

# Install scikit-learn using ONLY pre-built wheels (no compilation)
pip install scikit-learn --only-binary :all:
```

### Option 2: Use Latest Compatible Versions

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install with flexible versions (will use latest compatible with wheels)
pip install -r requirements.txt --only-binary :all:
```

### Option 3: Install Microsoft C++ Build Tools

1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++" workload
3. Restart terminal
4. Run: `pip install -r requirements.txt`

### Option 4: Use Python 3.10 or 3.11

Newer Python versions have better wheel support:

```powershell
# If you have Python 3.10 or 3.11 installed
python3.10 -m venv venv
# or
python3.11 -m venv venv
```

## Verify Installation

```powershell
python -c "import fastapi, sklearn, pandas, numpy; print('All packages installed successfully!')"
```

## Run the Server

```powershell
python -m app.main
```

---

**Recommended: Use Option 1 - it's the fastest and doesn't require installing build tools!**






