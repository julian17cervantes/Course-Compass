import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHIM = "HS256"
TOKE_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_access_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKE_EXPIRE_MINUTES)
    return jwt.encode({"sub": email, "exp":expire}, SECRET_KEY, algorithm=ALGORITHIM)