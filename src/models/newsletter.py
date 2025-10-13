"""
Newsletter subscription models and data storage.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
import json
import os
from pathlib import Path


class NewsletterSubscription(BaseModel):
    """Newsletter subscription model."""
    email: EmailStr
    location: str
    subscribed_at: datetime
    is_active: bool = True
    last_email_sent: Optional[datetime] = None


class NewsletterData:
    """Simple file-based storage for newsletter subscriptions."""
    
    def __init__(self, data_file: str = "data/newsletter_subscriptions.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(exist_ok=True)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the data file exists."""
        if not self.data_file.exists():
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def _load_subscriptions(self) -> List[dict]:
        """Load subscriptions from file."""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_subscriptions(self, subscriptions: List[dict]):
        """Save subscriptions to file."""
        with open(self.data_file, 'w') as f:
            json.dump(subscriptions, f, indent=2, default=str)
    
    def add_subscription(self, email: str, location: str) -> bool:
        """Add a new subscription."""
        subscriptions = self._load_subscriptions()
        
        # Check if email already exists
        for sub in subscriptions:
            if sub.get('email') == email:
                return False  # Already subscribed
        
        # Add new subscription
        new_subscription = {
            'email': email,
            'location': location,
            'subscribed_at': datetime.utcnow().isoformat(),
            'is_active': True,
            'last_email_sent': None
        }
        
        subscriptions.append(new_subscription)
        self._save_subscriptions(subscriptions)
        return True
    
    def get_active_subscriptions(self) -> List[NewsletterSubscription]:
        """Get all active subscriptions."""
        subscriptions = self._load_subscriptions()
        active_subs = []
        
        for sub in subscriptions:
            if sub.get('is_active', True):
                try:
                    active_subs.append(NewsletterSubscription(
                        email=sub['email'],
                        location=sub['location'],
                        subscribed_at=datetime.fromisoformat(sub['subscribed_at']),
                        is_active=sub.get('is_active', True),
                        last_email_sent=datetime.fromisoformat(sub['last_email_sent']) if sub.get('last_email_sent') else None
                    ))
                except (KeyError, ValueError) as e:
                    print(f"Error parsing subscription: {e}")
                    continue
        
        return active_subs
    
    def update_last_email_sent(self, email: str):
        """Update the last email sent timestamp for a subscription."""
        subscriptions = self._load_subscriptions()
        
        for sub in subscriptions:
            if sub.get('email') == email:
                sub['last_email_sent'] = datetime.utcnow().isoformat()
                break
        
        self._save_subscriptions(subscriptions)
    
    def unsubscribe(self, email: str) -> bool:
        """Unsubscribe an email."""
        subscriptions = self._load_subscriptions()
        
        for sub in subscriptions:
            if sub.get('email') == email:
                sub['is_active'] = False
                self._save_subscriptions(subscriptions)
                return True
        
        return False
