# Windows Installation Guide

## Issue: scikit-learn Build Error

If you encounter the error:
```
Microsoft Visual C++ 14.0 or greater is required
```

This happens because scikit-learn 1.3.2 tries to build from source on Windows.

## Solution

The requirements.txt has been updated to use versions with pre-built wheels. Follow these steps:

### Step 1: Clean Installation

```powershell
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip first (important for wheel support)
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 2: If Still Having Issues

If you still get build errors, install packages one by one:

```powershell
# Install core packages first
pip install fastapi uvicorn[standard] python-multipart
pip install pydantic pydantic-settings
pip install python-jose[cryptography] passlib[bcrypt]
pip install PyPDF2

# Install ML packages (these should use pre-built wheels)
pip install numpy
pip install pandas
pip install scikit-learn
```

### Step 3: Alternative - Use Conda (If pip fails)

If pip continues to fail, use conda which handles binary dependencies better:

```powershell
# Install conda if you don't have it
# Then create environment:
conda create -n career-platform python=3.10
conda activate career-platform
conda install scikit-learn pandas numpy
pip install -r requirements.txt
```

### Step 4: Verify Installation

```powershell
python -c "import fastapi; print('FastAPI OK')"
python -c "import sklearn; print('scikit-learn OK')"
python -c "import pandas; print('pandas OK')"
```

### Step 5: Run the Server

```powershell
python -m app.main
```

## Why This Happens

- Older versions of scikit-learn (like 1.3.2) may not have pre-built wheels for your Python version
- Building from source requires Microsoft Visual C++ Build Tools
- Newer versions (1.4.0+) have better wheel support for Windows

## Alternative: Install Build Tools

If you prefer to keep exact versions, you can install Microsoft C++ Build Tools:

1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++" workload
3. Then run: `pip install -r requirements.txt`

But using newer versions with wheels is easier and faster!






