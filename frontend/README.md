# Frontend Deployment Guide

## Environment Variables for Vercel

### Required Environment Variable (Production Only)

**VITE_API_BASE_URL** - Backend API base URL for production

**Production Value:**
```
VITE_API_BASE_URL=https://ai-career-backend-88xp.onrender.com/api/v1
```

### Setting Environment Variables in Vercel

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add the following variable:
   - **Name:** `VITE_API_BASE_URL`
   - **Value:** `https://ai-career-backend-88xp.onrender.com/api/v1`
   - **Environment:** `Production` (and optionally `Preview`/`Development`)

### Development vs Production

- **Development:** Uses `http://localhost:8000/api/v1` automatically
- **Production:** Requires `VITE_API_BASE_URL` environment variable
- **No fallback URLs** in production - must set environment variable

### Important Notes

- The active API URL is logged to the console on app startup
- All API calls use the shared axios instance exclusively
- No hardcoded localhost URLs in production
- No manual fetch/axios calls bypass the API service
