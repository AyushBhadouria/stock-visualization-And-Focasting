from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.config.mongodb import users_collection
from app.services.auth_service import AuthService
from datetime import timedelta
import hashlib

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    try:
        print(f"Registration attempt for: {user.email}")
        
        # Check if user exists
        existing_user = users_collection.find_one({"email": user.email})
        if existing_user:
            print(f"User already exists: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password with SHA256
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        print(f"Password hashed successfully")
        
        # Create user
        user_doc = {
            "email": user.email,
            "password_hash": hashed_password,
            "is_active": True,
            "is_premium": False
        }
        
        result = users_collection.insert_one(user_doc)
        print(f"User created with ID: {result.inserted_id}")
        
        # Create token
        access_token_expires = timedelta(minutes=30)
        access_token = auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        print(f"Token created successfully")
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    try:
        print(f"Login attempt for: {user.email}")
        
        # Find user
        db_user = users_collection.find_one({"email": user.email})
        if not db_user:
            print(f"User not found: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        hashed_input = hashlib.sha256(user.password.encode()).hexdigest()
        if hashed_input != db_user["password_hash"]:
            print(f"Password mismatch for: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        access_token_expires = timedelta(minutes=30)
        access_token = auth_service.create_access_token(
            data={"sub": db_user["email"]}, expires_delta=access_token_expires
        )
        print(f"Login successful for: {user.email}")
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        print(f"Verifying token: {credentials.credentials[:20]}...")
        email = auth_service.verify_token(credentials.credentials)
        if email is None:
            print("Token verification failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        print(f"Token verified for email: {email}")
        user = users_collection.find_one({"email": email})
        if user is None:
            print(f"User not found in database: {email}")
            # Create user if not exists (for testing)
            user = {
                "email": email,
                "password_hash": "dummy",
                "is_active": True,
                "is_premium": False
            }
            result = users_collection.insert_one(user)
            user["_id"] = result.inserted_id
            print(f"Created new user: {email}")
        
        print(f"User found: {user['email']}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Auth error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "is_premium": current_user.get("is_premium", False)
    }