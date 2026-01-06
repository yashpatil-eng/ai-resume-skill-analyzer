# 🚀 AI Career Intelligence Platform - Deployment Guide

This guide covers deployment to Railway and Render platforms.

## Table of Contents
- [Railway Deployment](#railway-deployment)
- [Render Deployment](#render-deployment)
- [Environment Variables](#environment-variables)
- [Frontend Deployment](#frontend-deployment)
- [Troubleshooting](#troubleshooting)

## Railway Deployment

### Prerequisites
- Railway account
- Supabase project set up
- Frontend deployed (Vercel/Netlify recommended)

### Steps

1. **Connect Repository**
   - Go to [Railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Environment Variables**
   - Go to your Railway project dashboard
   - Navigate to "Variables" tab
   - Add the following variables (see `railway-env-example.txt`):

3. **Deploy**
   - Railway will automatically detect the configuration and deploy
   - The build process will install dependencies and start the server

4. **Verify Deployment**
   - Check the deployment logs in Railway dashboard
   - Visit your Railway URL to test the API

## Render Deployment

### Prerequisites
- Render account
- Supabase project set up
- Frontend deployed (Vercel/Netlify recommended)

### Steps

1. **Connect Repository**
   - Go to [Render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: ai-career-backend
   - **Runtime**: Python 3
   - **Build Command**: `bash render-build.sh`
   - **Start Command**: `bash start.sh`

3. **Environment Variables**
   - Add the following environment variables (see `render-env-example.txt`):

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your application

5. **Verify Deployment**
   - Check the deployment logs
   - Visit your Render URL to test the API

## Environment Variables

### Required Variables

```bash
# Database (Supabase)
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Security
SECRET_KEY=your-very-secure-random-secret-key

# CORS (comma-separated URLs)
CORS_ORIGINS=https://your-frontend-domain.com

# Application
ENVIRONMENT=production
ALLOWED_HOSTS=your-deployment-domain.com
```

### Security Notes
- Generate a secure `SECRET_KEY` (use `openssl rand -hex 32`)
- Set specific `CORS_ORIGINS` for production security
- Never commit `.env` files to version control

## Frontend Deployment

### Vercel (Recommended)
1. Connect your frontend repository to Vercel
2. Set environment variable: `VITE_API_BASE_URL=https://your-backend-url`
3. Deploy

### Netlify
1. Connect your frontend repository to Netlify
2. Set environment variable: `VITE_API_BASE_URL=https://your-backend-url`
3. Deploy

## Troubleshooting

### Common Issues

#### Railway Issues
- **Build Fails**: Check that `railway-build.sh` has execute permissions
- **Port Issues**: Railway automatically sets `$PORT`
- **Memory Issues**: Upgrade Railway plan if needed

#### Render Issues
- **Python Version**: Ensure `runtime.txt` specifies compatible version
- **ML Libraries**: Render may use different Python versions - check build logs
- **Timeout**: Increase health check timeout in service settings

#### General Issues
- **CORS Errors**: Verify `CORS_ORIGINS` includes your frontend URL
- **Database Connection**: Check Supabase RLS policies
- **Environment Variables**: Ensure all required variables are set

### Logs
- **Railway**: Check logs in Railway dashboard
- **Render**: Check logs in Render service dashboard
- Use `print()` statements in build scripts for debugging

### Support
- Railway: [docs.railway.app](https://docs.railway.app)
- Render: [docs.render.com](https://docs.render.com)
- Supabase: [supabase.com/docs](https://supabase.com/docs)

