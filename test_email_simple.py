"""
Simple test to check if email system is working.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.welcome_email_service import WelcomeEmailService

def test_email_credentials():
    """Test if email credentials are configured."""
    print("🔧 Testing Email Configuration...")
    
    # Check environment variables
    smtp_server = os.getenv("SMTP_SERVER", "")
    smtp_port = os.getenv("SMTP_PORT", "")
    sender_email = os.getenv("SENDER_EMAIL", "")
    sender_password = os.getenv("SENDER_PASSWORD", "")
    sender_name = os.getenv("SENDER_NAME", "")
    
    print(f"SMTP_SERVER: {'✅ Set' if smtp_server else '❌ Not set'}")
    print(f"SMTP_PORT: {'✅ Set' if smtp_port else '❌ Not set'}")
    print(f"SENDER_EMAIL: {'✅ Set' if sender_email else '❌ Not set'}")
    print(f"SENDER_PASSWORD: {'✅ Set' if sender_password else '❌ Not set'}")
    print(f"SENDER_NAME: {'✅ Set' if sender_name else '❌ Not set'}")
    
    if not all([smtp_server, smtp_port, sender_email, sender_password]):
        print("\n❌ Email credentials not fully configured!")
        print("Please set these environment variables on Render:")
        print("SMTP_SERVER = smtp.gmail.com")
        print("SMTP_PORT = 587")
        print("SENDER_EMAIL = edgefindernews@gmail.com")
        print("SENDER_PASSWORD = ufzn fneg awxz jivh")
        print("SENDER_NAME = EdgeFinder")
        return False
    
    print("\n✅ All email credentials are configured!")
    return True

def test_welcome_email_generation():
    """Test welcome email generation without sending."""
    print("\n📧 Testing Welcome Email Generation...")
    
    try:
        welcome_service = WelcomeEmailService()
        
        # Test HTML generation
        html_content = welcome_service._create_welcome_html("TestUser", "Seattle, WA", {
            'best_odds': {
                'game': 'Lakers vs Warriors',
                'robinhood': '54% (Lakers win)',
                'sportsbook': '48%',
                'discrepancy': '6%'
            },
            'most_popular': {
                'game': 'Cowboys vs Eagles',
                'sportsbook': '-4.5 (Cowboys)',
                'volume': '32% of total handle'
            },
            'long_shot': {
                'game': 'Chicago Bulls +550',
                'robinhood': '0.15 (15%)',
                'payout': '5x+'
            }
        })
        
        print(f"✅ Generated HTML content: {len(html_content)} characters")
        
        # Test text generation
        text_content = welcome_service._create_welcome_text("TestUser", "Seattle, WA", {
            'best_odds': {
                'game': 'Lakers vs Warriors',
                'robinhood': '54% (Lakers win)',
                'sportsbook': '48%',
                'discrepancy': '6%'
            },
            'most_popular': {
                'game': 'Cowboys vs Eagles',
                'sportsbook': '-4.5 (Cowboys)',
                'volume': '32% of total handle'
            },
            'long_shot': {
                'game': 'Chicago Bulls +550',
                'robinhood': '0.15 (15%)',
                'payout': '5x+'
            }
        })
        
        print(f"✅ Generated text content: {len(text_content)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating welcome email: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Email System...")
    print("=" * 50)
    
    # Test credentials
    credentials_ok = test_email_credentials()
    
    # Test email generation
    generation_ok = test_welcome_email_generation()
    
    print("\n" + "=" * 50)
    if credentials_ok and generation_ok:
        print("✅ Email system is ready!")
        print("\n📧 To test actual email sending:")
        print("   1. Subscribe to newsletter on website")
        print("   2. Check email for welcome message")
        print("   3. Check spam folder if not received")
    else:
        print("❌ Email system needs configuration")
        print("\n🔧 Next steps:")
        print("   1. Configure email credentials on Render")
        print("   2. Test newsletter signup on website")
        print("   3. Check Render logs for email errors")
