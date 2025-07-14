import jwt
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

class JWTManager:
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or os.getenv('JWT_SECRET_KEY', 'your-fallback-secret-key-change-this')
        self.algorithm = 'HS256'
        self.default_expiration_hours = 24
    
    def create_token(self, user_email: str, user_id: Optional[str] = None, expires_in_hours: int = None) -> str:
        expiration_hours = expires_in_hours or self.default_expiration_hours
        
        payload = {
            "email": user_email,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=expiration_hours),
            "type": "access_token"
        }
        
        if user_id:
            payload["user_id"] = str(user_id)
        
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
        except Exception as e:
            raise ValueError(f"Failed to create token: {str(e)}")
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                options={
                    "verify_exp": True,  
                    "verify_iat": True, 
                    "require": ["exp", "iat", "email"]
                }
            )
            return payload
            
        except jwt.ExpiredSignatureError:
            print("❌ Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"❌ Invalid token: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Token verification error: {str(e)}")
            return None
    
    def is_token_valid(self, token: str) -> bool:
        return self.verify_token(token) is not None

    
    def create_refresh_token(self, user_email: str, user_id: Optional[str] = None) -> str:
        payload = {
            "email": user_email,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=30),
            "type": "refresh_token"
        }
        
        if user_id:
            payload["user_id"] = str(user_id)
        
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
        except Exception as e:
            raise ValueError(f"Failed to create refresh token: {str(e)}")
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        payload = self.verify_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh_token":
            return None
        
        return self.create_token(
            user_email=payload["email"],
            user_id=payload.get("user_id")
        )

jwt_manager = JWTManager()