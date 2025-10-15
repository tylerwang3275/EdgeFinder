"""
Test the complete email system to verify it's working.
"""

import requests
import json

def test_newsletter_signup_with_welcome():
    """Test newsletter signup and check if welcome email is sent."""
    url = "https://edgefinder-czi3.onrender.com/api/newsletter/subscribe"
    
    # Use a unique test email
    import time
    timestamp = int(time.time())
    test_email = f"test{timestamp}@example.com"
    
    test_data = {
        "email": test_email,
        "location": "Seattle, WA",
        "terms": True
    }
    
    print(f"🧪 Testing newsletter signup with email: {test_email}")
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Newsletter signup successful!")
            print(f"   Welcome email sent: {result.get('welcome_sent', 'Unknown')}")
            
            # Check if email credentials are configured
            if result.get('welcome_sent') == False:
                print("⚠️ Welcome email not sent - likely email credentials not configured")
            elif result.get('welcome_sent') == True:
                print("✅ Welcome email should have been sent!")
        else:
            print("❌ Newsletter signup failed")
            
    except Exception as e:
        print(f"❌ Error testing newsletter signup: {e}")

def test_email_configuration():
    """Test if email configuration is working."""
    print("\n🔧 Testing email configuration...")
    
    # Test the newsletter send endpoint to see if emails work
    url = "https://edgefinder-czi3.onrender.com/api/newsletter/send"
    
    try:
        response = requests.post(url, timeout=30)
        print(f"Newsletter send status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Newsletter send successful!")
            print(f"   Emails sent: {result.get('emails_sent', 0)}")
            print(f"   Total subscribers: {result.get('total_subscribers', 0)}")
        else:
            print("❌ Newsletter send failed")
            
    except Exception as e:
        print(f"❌ Error testing newsletter send: {e}")

def check_subscribers():
    """Check current subscribers."""
    print("\n📊 Checking current subscribers...")
    
    url = "https://edgefinder-czi3.onrender.com/api/newsletter/subscribers"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Subscribers status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Total subscribers: {result.get('total_subscribers', 0)}")
            
            for sub in result.get('subscribers', []):
                print(f"   - {sub['email']} from {sub['location']}")
        else:
            print("❌ Failed to get subscribers")
            
    except Exception as e:
        print(f"❌ Error checking subscribers: {e}")

if __name__ == "__main__":
    print("🚀 Testing Complete Email System...")
    print("=" * 50)
    
    test_newsletter_signup_with_welcome()
    test_email_configuration()
    check_subscribers()
    
    print("\n" + "=" * 50)
    print("📧 If welcome emails aren't working:")
    print("   1. Check if email credentials are configured on Render")
    print("   2. Verify SMTP settings are correct")
    print("   3. Check Render logs for email errors")
