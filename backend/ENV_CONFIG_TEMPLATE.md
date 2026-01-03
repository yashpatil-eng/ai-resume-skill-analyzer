# AI Career Intelligence Platform - Environment Configuration Template

## Required Environment Variables

Copy these to your Render environment variables section:

### Supabase Configuration
```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key-here
```

### Application Settings
```
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### File Upload Settings
```
MAX_UPLOAD_SIZE_MB=10
ALLOWED_FILE_TYPES=pdf
```

### AI/ML Settings
```
JOBS_DATASET_PATH=../dataset/jobs.csv
```

### Development Settings
```
DEBUG=False
ENVIRONMENT=production
```

## How to Set Up Environment Variables in Render

1. Go to your Render service dashboard
2. Click on "Environment"
3. Add each variable from the list above
4. Use the actual values from your Supabase project
5. Generate a secure SECRET_KEY (you can use: `openssl rand -hex 32`)

## Security Notes

- Never commit actual values to version control
- Keep SUPABASE_SERVICE_ROLE_KEY secure
- Use strong, unique SECRET_KEY for JWT tokens
- Rotate keys periodically for security

## Getting Supabase Keys

1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to Settings → API
4. Copy the Project URL and anon/public key
5. For service role key, go to Settings → API → Service Role Key
