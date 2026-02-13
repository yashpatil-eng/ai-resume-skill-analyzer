"""
Main FastAPI application entry point
AI-Driven Career Intelligence & Employability Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
import os

from app.core.config import settings
from app.routes import auth, resume, recommend

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Driven Career Intelligence & Employability Platform - Phase 1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure security and CORS based on environment
environment = os.getenv("ENVIRONMENT", "production")

# CORS configuration
cors_origins = settings.CORS_ORIGINS

# In development, allow common dev origins; in production, use specific origins
if not cors_origins:
    if environment == "development" or settings.VERSION == "dev":
        cors_origins = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"]
    else:
        # For production, you should set CORS_ORIGINS in environment variables
        # Default to empty list for security - configure this properly in production
        cors_origins = []

# Add security middleware
if environment == "production":
    # In production, trust specific hosts (configure via environment)
    allowed_hosts = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else ["*"]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Add CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-resume-skill-analyzer.vercel.app",
        "https://ai-resume-skill-analyzer-ipgh97scw.vercel.app",  # optional preview
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],   # allow all methods OR replace with explicit list
    allow_headers=["*"],   # allow all headers
)
# Include routers
print("=== STARTING ROUTER INCLUSION ===")
print("Testing routers import...")
try:
    from app.routes import auth, resume, recommend
    print("[SUCCESS] Routers imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import routers: {e}")
    exit(1)

try:
    print(f"Including routers with prefix: {settings.API_V1_PREFIX}")
    app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
    app.include_router(resume.router, prefix=settings.API_V1_PREFIX)
    app.include_router(recommend.router, prefix=settings.API_V1_PREFIX)
    print("[SUCCESS] All routers included successfully")
except Exception as e:
    print(f"[ERROR] Failed to include routers: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("[SUCCESS] ROUTER INCLUSION COMPLETED")
print("Available API routes:")
for route in app.routes:
    if hasattr(route, 'path') and '/api/v1' in route.path:
        print(f"  {route.methods} {route.path}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI-Driven Career Intelligence & Employability Platform",
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME
    }


@app.post("/test-register")
async def test_register(email: str, password: str, full_name: str):
    """Simple test endpoint"""
    return {"message": f"Received: {email}, {full_name}"}


@app.post("/test-httpexception")
async def test_httpexception():
    """Test HTTPException handling"""
    from fastapi import HTTPException
    raise HTTPException(status_code=400, detail="Test HTTPException")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler - only catch non-HTTP exceptions"""
    from fastapi import HTTPException
    from starlette.exceptions import HTTPException as StarletteHTTPException

    # Let FastAPI handle HTTPExceptions
    if isinstance(exc, (HTTPException, StarletteHTTPException)):
        raise exc

    print(f"=== GLOBAL EXCEPTION HANDLER ===")
    print(f"Request: {request.method} {request.url}")
    print(f"Exception: {type(exc).__name__}: {exc}")
    import traceback
    traceback.print_exc()

    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.VERSION == "dev" else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
