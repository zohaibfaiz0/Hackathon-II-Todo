from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from pydantic import BaseModel, EmailStr

from ..auth.jwt import create_access_token
from ..config import settings
from ..services.user_service import (
    create_user,
    authenticate_user,
    get_user_by_email
)
from ..models.user import UserCreate

router = APIRouter()


class UserRegisterRequest(BaseModel):
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegisterRequest):
    """
    Register a new user
    """
    # Validate email format
    if "@" not in user_data.email or "." not in user_data.email.split("@")[-1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password length
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )

    if len(user_data.password) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be no more than 72 characters"
        )

    # Check if user exists
    existing = await get_user_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        # Create user in database
        user = await create_user(UserCreate(
            email=user_data.email,
            password=user_data.password
        ))

        # Create access token with user ID
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        return TokenResponse(access_token=access_token, token_type="bearer")

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLoginRequest):
    """
    Login a user and return access token
    """
    user = await authenticate_user(credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token with user ID
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/auth/logout")
async def logout():
    """
    Logout a user (client-side token invalidation)
    Note: With JWT, actual invalidation happens client-side by removing the token.
    For production, consider implementing a token blacklist.
    """
    return {"message": "Logged out successfully"}