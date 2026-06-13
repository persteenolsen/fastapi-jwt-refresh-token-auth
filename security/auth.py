# from passlib.context import CryptContext

from pwdlib import PasswordHash

import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

from fastapi import HTTPException, status

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# 26-01-2026 - Added for refresh tokens
# Note: Refresh tokens should expire in days, not minutes !
# For testing purposes we are using only 5 minutes here
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    # return pwd_context.verify(plain_password, hashed_password)
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    # return pwd_context.hash(password)
    return password_hash.hash(password)

# Create JWT access token with expiration where data={"sub": username} received from main.py
def create_access_token(data: dict):
    to_encode = data.copy()
    
    # 26-01-2024 - Changed datetime.utcnow() to datetime.now()
    # For testing purposes we are using only 2 minutes here
    #expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 13-06-2026 - Added type for validation
    #to_encode.update({"exp": expire})
    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Create Refresh Yoken with expiration where data={"sub": username} received from main.py
def create_refresh_token(data: dict):
    to_encode = data.copy()
    
    # 26-01-2026 - Changed datetime.utcnow() to datetime.now()
    # Note: Refresh tokens should expire in days, not minutes !
    # For testing purposes we are using only 5 minutes here
    #expire = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    # 13-06-2026 - Added type for validation
    #to_encode.update({"exp": expire})
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT tokens (Access and Refresh Tokens) by:
# 1) Is valid and signed by the SECRET_KEY
# 2) Has not expired
# 3) Has a Username (sub claim)
# 4) Matches the expected token type (access or refresh), if specified
#
# Note: If the token is invalid, expired, missing required claims,
# or has the wrong type, None is returned.
def verify_token(token: str, expected_type: str = None):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        token_type = payload.get("type")

        # Username must exist
        if username is None:
            return None

        # Validate token type if specified
        if expected_type and token_type != expected_type:
            return None

        return username

    except jwt.ExpiredSignatureError:
        print("Token has expired!")
        return None

    except jwt.InvalidTokenError:
        print("Invalid token!")
        return None