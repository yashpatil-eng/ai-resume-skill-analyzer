# Environment Variables Setup Guide

## Quick Setup

### Option 1: Use the provided .env file
The `.env` file has been created in the `backend/` directory with default values for local development.

### Option 2: Create from template
1. Copy `env.example` to `.env`:
   ```powershell
   cd backend
   Copy-Item env.example .env
   ```

2. Update the values in `.env` as needed.

## Environment Variables Reference

### Required Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `SECRET_KEY` | Secret key for JWT token signing | Generated random key |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

### Optional Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `API_V1_PREFIX` | API route prefix | `/api/v1` |
| `PROJECT_NAME` | Application name | `AI Career Intelligence Platform` |
| `VERSION` | Application version | `1.0.0` |
| `DATABASE_URL` | PostgreSQL connection string | `None` |
| `SUPABASE_URL` | Supabase project URL | `None` |
| `SUPABASE_KEY` | Supabase API key | `None` |
| `MAX_UPLOAD_SIZE` | Maximum file upload size (bytes) | `10485760` (10MB) |
| `UPLOAD_DIR` | Directory for uploaded files | `uploads` |
| `DATASET_PATH` | Path to jobs CSV file | `dataset/jobs.csv` |
| `MIN_SIMILARITY_THRESHOLD` | Minimum similarity for recommendations | `0.1` |

## Generating a Secure Secret Key

For production, generate a secure secret key:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Or using Python:
```python
import secrets
print(secrets.token_urlsafe(32))
```

## Production Checklist

Before deploying to production:

- [ ] Generate a new `SECRET_KEY` (don't use the default)
- [ ] Set `DATABASE_URL` if using a database
- [ ] Set `SUPABASE_URL` and `SUPABASE_KEY` if using Supabase
- [ ] Adjust `MIN_SIMILARITY_THRESHOLD` based on your needs
- [ ] Set appropriate `MAX_UPLOAD_SIZE` for your use case
- [ ] Ensure `.env` is in `.gitignore` (already configured)

## Security Notes

1. **Never commit `.env` to version control** - it's already in `.gitignore`
2. **Use different keys for development and production**
3. **Keep your `SECRET_KEY` secure** - it's used for JWT token signing
4. **Rotate keys periodically** in production

## File Locations

- **Template**: `backend/env.example`
- **Local Config**: `backend/.env` (created automatically)
- **Git Ignore**: `.gitignore` (already configured)

## Troubleshooting

### .env file not being read

1. Make sure `.env` is in the `backend/` directory
2. Check that `pydantic-settings` is installed
3. Verify file encoding is UTF-8
4. Restart the server after changing `.env`

### Variables not taking effect

- Environment variables take precedence over `.env` file
- Check for typos in variable names (case-sensitive)
- Restart the server after changes






