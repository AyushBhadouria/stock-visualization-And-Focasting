from datetime import datetime, timedelta
from jose import JWTError, jwt
import hashlib
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.get_password_hash(plain_password) == hashed_password
    
    def get_password_hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str):
        try:
            print(f"Decoding token with secret: {SECRET_KEY[:10]}...")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            print(f"Token payload: {payload}")
            if email is None:
                print("No email in token payload")
                return None
            print(f"Token verified for: {email}")
            return email
        except JWTError as e:
            print(f"JWT Error: {str(e)}")
            return None
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return None