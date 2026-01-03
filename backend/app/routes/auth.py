"""
Authentication routes for user registration and login
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import uuid

from app.models.schemas import UserRegister, UserLogin, TokenResponse
from app.core.config import settings
from app.services.database import DatabaseService

router = APIRouter(prefix="/auth", tags=["Authentication"])

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def hash_password(password: str) -> str:
    """Hash password using SHA-256 (use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Get user from database
    user = await DatabaseService.get_user_by_email(email)
    if not user:
        raise credentials_exception

    return user


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user

    Returns:
        JWT access token and user information
    """
    # Check if user already exists
    existing_user = await DatabaseService.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    password_hash = hash_password(user_data.password)
    user = await DatabaseService.create_user(
        user_data.email,
        password_hash,
        user_data.full_name
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email, "user_id": str(user['user_id'])},
        expires_delta=access_token_expires
    )

    # Store session in database
    from app.services.database import DatabaseService
    import uuid
    from datetime import datetime, timedelta

    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Note: We're not actually storing sessions in database yet
    # This is just for future implementation
    print(f"Session created for user {user_data.email}: {session_id}")

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user['user_id']),
        email=user_data.email
    )


@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin):
    """
    Login user and return JWT token
    """
    email = user_credentials.email

    # Check if user exists
    user = await DatabaseService.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email, "user_id": str(user["user_id"])},
        expires_delta=access_token_expires
    )

    # Store session in database
    from app.services.database import DatabaseService
    import uuid
    from datetime import datetime, timedelta

    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Note: We're not actually storing sessions in database yet
    # This is just for future implementation
    print(f"Login session created for user {email}: {session_id}")

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user["user_id"]),
        email=email
    )


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information
    """
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "full_name": current_user["full_name"]
    }



