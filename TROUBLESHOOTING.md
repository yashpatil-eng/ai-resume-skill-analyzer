# Troubleshooting Guide

## Common Issues and Solutions

### Backend Issues

#### 1. **ModuleNotFoundError: No module named 'app'**

**Error:**
```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
- Make sure you're running from the `backend` directory
- Use: `python -m app.main` (not `python app/main.py`)
- Or use: `uvicorn app.main:app --reload`

#### 2. **Dataset Not Found Error**

**Error:**
```
FileNotFoundError: Jobs dataset not found
```

**Solution:**
- Ensure `dataset/jobs.csv` exists in the project root (not in backend/)
- The file structure should be:
  ```
  Project/
  ├── backend/
  ├── dataset/
  │   └── jobs.csv  ← Should be here
  └── frontend/
  ```
- Run the backend from the project root or backend directory

#### 3. **Pydantic Configuration Error**

**Error:**
```
AttributeError: type object 'Settings' has no attribute 'Config'
```

**Solution:**
- This is fixed in the latest version
- Make sure you have `pydantic-settings==2.1.0` installed
- Run: `pip install --upgrade pydantic-settings`

#### 4. **Port Already in Use**

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
- Change the port: `uvicorn app.main:app --port 8001`
- Or kill the process using port 8000:
  - Windows: `netstat -ano | findstr :8000` then `taskkill /PID <pid> /F`
  - Mac/Linux: `lsof -ti:8000 | xargs kill`

#### 5. **Import Errors**

**Error:**
```
ImportError: cannot import name 'X' from 'Y'
```

**Solution:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment
- Check Python version (requires Python 3.8+)

#### 6. **CORS Errors**

**Error:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
- Backend CORS is already configured to allow all origins
- Make sure backend is running on port 8000
- Check frontend API URL in `frontend/src/services/api.js`

### Frontend Issues

#### 1. **Module Not Found**

**Error:**
```
Module not found: Can't resolve 'X'
```

**Solution:**
- Delete `node_modules` and `package-lock.json`
- Run: `npm install`
- Make sure you're in the `frontend` directory

#### 2. **Port Already in Use**

**Error:**
```
Port 3000 is in use
```

**Solution:**
- Vite will automatically use the next available port
- Check terminal for the actual port number
- Or specify: `npm run dev -- --port 3001`

#### 3. **API Connection Failed**

**Error:**
```
Network Error or Failed to fetch
```

**Solution:**
- Make sure backend is running on `http://localhost:8000`
- Check `frontend/src/services/api.js` for correct API URL
- Verify CORS is enabled in backend
- Check browser console for detailed error

#### 4. **Authentication Errors**

**Error:**
```
401 Unauthorized
```

**Solution:**
- Make sure you're logged in
- Check if token is stored in localStorage
- Try logging out and logging in again
- Clear browser cache and localStorage

#### 5. **Resume Upload Fails**

**Error:**
```
Failed to upload resume
```

**Solution:**
- Ensure file is a PDF (not Word doc or image)
- Check file size (max 10MB)
- Verify backend is running
- Check browser console for detailed error

### Dataset Issues

#### 1. **CSV File Not Found**

**Solution:**
- Create `dataset/jobs.csv` in project root if missing
- Verify file has columns: `job_id`, `job_title`, `skills`
- Check file encoding (should be UTF-8)

#### 2. **Empty Recommendations**

**Solution:**
- Check if skills are being extracted from resume
- Verify job dataset has matching skills
- Lower the similarity threshold in config if needed

### General Issues

#### 1. **Virtual Environment Not Activated**

**Solution:**
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`
- You should see `(venv)` in your terminal prompt

#### 2. **Python Version Issues**

**Solution:**
- Requires Python 3.8 or higher
- Check: `python --version`
- Use Python 3.8+ if needed

#### 3. **Node Version Issues**

**Solution:**
- Requires Node.js 16 or higher
- Check: `node --version`
- Update Node.js if needed

## Quick Diagnostic Commands

### Backend
```bash
# Check Python version
python --version

# Check if dependencies are installed
pip list | grep fastapi

# Test import
python -c "from app.main import app; print('OK')"

# Check if dataset exists
python -c "import os; print(os.path.exists('dataset/jobs.csv'))"
```

### Frontend
```bash
# Check Node version
node --version

# Check if dependencies are installed
npm list react

# Test build
npm run build
```

## Still Having Issues?

1. **Check Logs:**
   - Backend: Check terminal output
   - Frontend: Check browser console (F12)

2. **Verify Setup:**
   - Follow QUICKSTART.md step by step
   - Make sure all prerequisites are installed

3. **Common Fixes:**
   - Restart both servers
   - Clear browser cache
   - Delete and reinstall dependencies
   - Check file paths and structure

4. **Get Help:**
   - Check API docs at http://localhost:8000/docs
   - Review architecture.md for system design
   - Check README.md for detailed instructions

---

**If you're still stuck, share the exact error message and I'll help you fix it!**






