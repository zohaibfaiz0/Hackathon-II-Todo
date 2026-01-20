from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from ..auth.jwt import create_access_token
from ..config import settings
from pydantic import BaseModel
from typing import Optional
import hashlib
import secrets
import uuid

router = APIRouter()



class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


fake_users_db = {}  # In reality, you'd have a proper user model and database


def hash_password_with_salt(password: str) -> tuple[str, str]:
    """Generate a salt and hash the password with SHA-256"""
    salt = secrets.token_hex(32)  # Generate a random 32-byte salt
    pwdhash = hashlib.pbkdf2_hmac('sha256',
                                  password.encode('utf-8'),
                                  salt.encode('utf-8'),
                                  100000)  # Use 100,000 iterations
    pwdhash = pwdhash.hex()
    return pwdhash, salt


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    """Verify a password against its hash and salt"""
    pwdhash = hashlib.pbkdf2_hmac('sha256',
                                  plain_password.encode('utf-8'),
                                  salt.encode('utf-8'),
                                  100000)
    pwdhash = pwdhash.hex()
    return pwdhash == hashed_password


def authenticate_user(email: str, password: str):
    # In a real implementation, this would query the database
    if email in fake_users_db:
        user = fake_users_db[email]
        if verify_password(password, user["hashed_password"], user["salt"]):
            return user
    return None


@router.post("/auth/register", response_model=Token)
async def register(user: UserCreate):
    """
    Register a new user
    """
    # Check if user already exists
    if user.email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate email format (basic validation)
    if "@" not in user.email or "." not in user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password length
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )

    # Hash the password with salt
    hashed_password, salt = hash_password_with_salt(user.password)

    # Create user in "database"
    user_id = str(uuid.uuid4())
    fake_users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_password,
        "salt": salt
    }

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """
    Login a user and return access token
    """
    user = authenticate_user(user_credentials.email, user_credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/logout")
async def logout():
    """
    Logout a user (client-side token invalidation)
    """
    # In a real implementation, you might add the token to a blacklist
    return {"message": "Logged out successfully"}