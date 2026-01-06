# Frontend Deployment Guide

## Environment Variables for Vercel

### Required Environment Variable

**VITE_API_BASE_URL** - Backend API base URL

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

### Local Development

For local development, create a `.env.local` file:

```bash
# .env.local (for local development only)
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Important Notes

- The frontend will throw an error if `VITE_API_BASE_URL` is not defined
- No fallback URLs are used - the environment variable must be set
- The active API URL is logged to the console on app startup
- All API calls use this base URL exclusively
