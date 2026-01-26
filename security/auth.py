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

    to_encode.update({"exp": expire})
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

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT tokens (JWT Access + Refresh Tokens) by:
# 1) Is valid signed by the SECRET_KEY
# 2) Has a Username
# 3) Has not expired
# Note: If the token is invalid or expired (2 and 5 minutes for testing and demo), None is returned
def verify_token(token: str):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 24-01-2026 - Added for refresh tokens
        # There will be an exception if the token has expired
        expire: datetime = payload.get("exp")
        if expire is None:
           return None
        
       # Print current datetime and UTC now for debugging        
        current = datetime.now()
        print("Current datetime:", str(current))
        
        # locally its 1 hour behind the current time
        utcnow = datetime.now(timezone.utc)
        print("UTC now:", utcnow)
        
        # Just testing - PyJWT will raise an exception if the token has expired 
        # and this code will not be reached
        # datetime.utcnow()
        if datetime.now() < datetime.fromtimestamp(expire):
           print("The Token has not yet expired !")
          
           
        username: str = payload.get("sub")
        if username is None:
           return None
       
        return username
            
    except jwt.PyJWTError:
        print("The Token has expired or another PyJWT Exception occured !")
        return None
       