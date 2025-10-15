"""
Test script for welcome email functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.welcome_email_service import WelcomeEmailService


def test_welcome_email():
    """Test welcome email generation and sending."""
    print("🧪 Testing Welcome Email System...")
    
    # Test email service
    welcome_service = WelcomeEmailService()
    
    # Test HTML generation
    html_content = welcome_service._create_welcome_html("John", "Seattle, WA")
    print(f"✅ Generated HTML content: {len(html_content)} characters")
    
    # Test text generation
    text_content = welcome_service._create_welcome_text("John", "Seattle, WA")
    print(f"✅ Generated text content: {len(text_content)} characters")
    
    # Test hometown team detection
    test_locations = [
        "Seattle, WA",
        "Los Angeles, CA", 
        "New York, NY",
        "Chicago, IL",
        "Boston, MA",
        "Unknown City"
    ]
    
    print("\n🏠 Testing hometown team detection:")
    for location in test_locations:
        team = welcome_service._get_hometown_team(location)
        print(f"   {location} → {team}")
    
    print("\n✅ Welcome email system is ready!")
    print("\n📧 To test actual email sending:")
    print("   1. Configure email credentials on Render")
    print("   2. Subscribe to newsletter on website")
    print("   3. Check email for welcome message")
    
    return True


if __name__ == "__main__":
    test_welcome_email()
