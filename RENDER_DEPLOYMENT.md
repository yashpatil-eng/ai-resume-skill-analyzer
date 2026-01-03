# 🚀 Render Deployment Guide

## AI Career Intelligence Platform - Render Deployment

This guide will help you deploy your AI Career Intelligence Platform to Render successfully.

## Prerequisites

- GitHub repository with your project
- Supabase account and project
- Render account

## Step 1: Prepare Your Repository

Your repository has been optimized for Render deployment with:
- ✅ Updated `requirements.txt` with compatible versions
- ✅ `runtime.txt` specifying Python 3.12.7 (ML library compatible)
- ✅ `build.sh` script for proper ML library installation
- ✅ Environment configuration template

## Step 2: Create Render Web Service

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New" → "Web Service"

2. **Connect Repository**
   - Connect your GitHub account
   - Select your `ai-career-intelligence-platform` repository
   - Choose the `main` branch

3. **Configure Service**
   ```
   Name: ai-career-intelligence-platform
   Environment: Python 3
   Build Command: ./build.sh
   Start Command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

## Step 3: Set Environment Variables

Add these environment variables in Render (go to your service → Environment):

### Required Variables
```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key-here
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
```

### Optional Variables
```
DEBUG=False
ENVIRONMENT=production
MAX_UPLOAD_SIZE_MB=10
ALLOWED_FILE_TYPES=pdf
JOBS_DATASET_PATH=../dataset/jobs.csv
```

## Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. The build process will:
   - Use Python 3.11.8
   - Force binary installation of ML libraries
   - Install all dependencies
   - Verify critical imports
   - Start the FastAPI server

## Step 5: Verify Deployment

1. **Check Build Logs**
   - Go to your service logs
   - Verify no compilation errors
   - Confirm ML libraries installed successfully

2. **Test API Endpoints**
   - Visit `https://your-service-name.onrender.com/docs`
   - Test the `/auth/register` endpoint
   - Try uploading a resume and getting recommendations

3. **Frontend Deployment** (Optional)
   - Deploy frontend to Vercel/Netlify
   - Point it to your Render backend URL

## Troubleshooting

### Python Version Issues

**Issue: Render using Python 3.13.x instead of specified version**
```
Symptoms: Build fails with "Cython compilation errors" or "no module named 'int_t'"
Solution:
1. Ensure runtime.txt contains: python-3.12.7
2. The build.sh script is optimized for Python 3.12.7
3. If issues persist, check Render's Python version support
```

**Issue: ML library installation fails**
```
Symptoms: "Could not find a version that satisfies the requirement"
Solution:
1. build.sh forces binary installation (--only-binary=all)
2. All ML libraries are pinned to compatible versions
3. Check build logs for specific error messages
```

### Build Failures

**Issue: scikit-learn compilation errors**
```
Solution: The build.sh script forces binary installation
```

**Issue: Import errors**
```
Check: Build logs for missing dependencies
Solution: All dependencies are pinned to compatible versions
```

**Issue: Memory errors during build**
```
Solution: Render's free tier should handle this, upgrade if needed
```

### Runtime Errors

**Issue: Database connection fails**
```
Check: SUPABASE_URL and keys are correct
Solution: Verify Supabase project is active
```

**Issue: File upload fails**
```
Check: JOBS_DATASET_PATH is correct
Solution: Ensure dataset/jobs.csv exists in repository
```

## Performance Optimization

### Free Tier Limitations
- 750 hours/month
- 512 MB RAM
- Auto-sleep after 15 minutes

### Cost Optimization
- Application will auto-sleep when not in use
- Consider upgrading to paid tier for production use

## Security Considerations

- ✅ JWT tokens with expiration
- ✅ Supabase Row Level Security
- ✅ Input validation with Pydantic
- ✅ Secure environment variable handling

## Monitoring

- **Logs**: Available in Render dashboard
- **Metrics**: Response times and error rates
- **Health Check**: Visit `/docs` to verify API is running

## Updating Your Deployment

1. Push changes to GitHub main branch
2. Render will automatically redeploy
3. Monitor logs for any issues

## Support

If you encounter issues:
1. Check Render build logs
2. Verify environment variables
3. Test locally with same Python version
4. Refer to project documentation

---

## 🎉 Successful Deployment Checklist

- [ ] Render service created
- [ ] Environment variables set
- [ ] Build completed without errors
- [ ] API accessible at `https://your-service.onrender.com/docs`
- [ ] Database connection working
- [ ] ML functionality operational
- [ ] Frontend deployed (optional)

**Your AI Career Intelligence Platform is now live on Render! 🚀**
