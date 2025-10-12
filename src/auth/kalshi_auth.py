"""
Kalshi JWT authentication module.
"""

import jwt
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from cryptography.hazmat.primitives import serialization


class KalshiAuth:
    """Handles JWT authentication for Kalshi API."""
    
    def __init__(self, api_key_id: str, private_key: str):
        """
        Initialize Kalshi authentication.
        
        Args:
            api_key_id: The API key ID from Kalshi
            private_key: The RSA private key in PEM format
        """
        self.api_key_id = api_key_id
        self.private_key = private_key
        self._jwt_token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
    
    def _load_private_key(self) -> Any:
        """Load the RSA private key."""
        try:
            # Handle both full PEM format and just the key content
            key_data = self.private_key
            if not key_data.startswith('-----BEGIN'):
                key_data = f"-----BEGIN RSA PRIVATE KEY-----\n{key_data}\n-----END RSA PRIVATE KEY-----"
            
            return serialization.load_pem_private_key(
                key_data.encode(),
                password=None
            )
        except Exception as e:
            raise ValueError(f"Failed to load private key: {e}")
    
    def _generate_jwt_token(self) -> str:
        """Generate a JWT token for Kalshi API authentication."""
        try:
            private_key = self._load_private_key()
            
            # JWT payload
            now = datetime.utcnow()
            payload = {
                'sub': self.api_key_id,  # Subject (API key ID)
                'iat': int(now.timestamp()),  # Issued at
                'exp': int((now + timedelta(hours=1)).timestamp()),  # Expires in 1 hour
                'iss': 'edgefinder',  # Issuer
                'aud': 'kalshi-api'  # Audience
            }
            
            # Generate JWT token
            token = jwt.encode(
                payload,
                private_key,
                algorithm='RS256',
                headers={'kid': self.api_key_id}  # Key ID
            )
            
            return token
            
        except Exception as e:
            raise ValueError(f"Failed to generate JWT token: {e}")
    
    def get_auth_token(self) -> str:
        """
        Get a valid authentication token.
        
        Returns:
            JWT token string
        """
        # Check if we have a valid token
        if (self._jwt_token and self._token_expires and 
            datetime.utcnow() < self._token_expires - timedelta(minutes=5)):
            return self._jwt_token
        
        # Generate new token
        self._jwt_token = self._generate_jwt_token()
        self._token_expires = datetime.utcnow() + timedelta(hours=1)
        
        return self._jwt_token
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary with Authorization header
        """
        token = self.get_auth_token()
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
