from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime
import warnings

from ..models.user import User, UserCreate
from ..database import get_async_session, AsyncSessionLocal

# Suppress the bcrypt version warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Configure bcrypt context with maximum compatibility
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    # Truncate password to 72 characters to comply with bcrypt limit
    truncated_password = password[:72] if len(password) > 72 else password
    try:
        return pwd_context.hash(truncated_password)
    except Exception as e:
        # Fallback for bcrypt compatibility issues
        import hashlib
        import secrets
        salt = secrets.token_hex(32)
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      truncated_password.encode('utf-8'),
                                      salt.encode('utf-8'),
                                      100000)
        pwdhash = pwdhash.hex()
        # Store as: salt$hash$pbkdf2 - putting salt first makes it easier to extract
        return f"{salt}${pwdhash}$pbkdf2"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Check if it's a pbkdf2 hash (has $pbkdf2$ suffix)
        if hashed_password.endswith('$pbkdf2'):
            # Extract salt and hash from the stored format: salt$hash$pbkdf2
            parts = hashed_password.split('$')
            if len(parts) >= 3:  # We expect: salt$hash$pbkdf2
                salt = parts[0]
                stored_hash = parts[1]

                # Recreate the hash with the same salt
                import hashlib
                pwdhash = hashlib.pbkdf2_hmac('sha256',
                                              plain_password.encode('utf-8'),
                                              salt.encode('utf-8'),
                                              100000)
                pwdhash = pwdhash.hex()

                return pwdhash == stored_hash

        # Use bcrypt for regular hashes (including bcrypt's own salt handling)
        return pwd_context.verify(plain_password, hashed_password)
    except:
        # Fallback for bcrypt compatibility issues
        return False


async def get_user_by_email(email: str) -> Optional[User]:
    async with AsyncSessionLocal() as session:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()


async def get_user_by_id(user_id: int) -> Optional[User]:
    async with AsyncSessionLocal() as session:
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()


async def create_user(user_data: UserCreate) -> User:
    # First, check if user exists in a separate session to avoid nesting
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise ValueError("Email already registered")

    # Now create the user in a new session
    async with AsyncSessionLocal() as session:
        # Double-check within the same session to avoid race conditions
        statement = select(User).where(User.email == user_data.email)
        result = await session.execute(statement)
        existing = result.scalar_one_or_none()
        if existing:
            raise ValueError("Email already registered")

        # Create new user
        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user