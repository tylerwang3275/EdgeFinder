"""
Debug email system to see what's happening.
"""

import requests
import json
import time

def test_newsletter_signup():
    """Test newsletter signup with a unique email."""
    url = "https://edgefinder-czi3.onrender.com/api/newsletter/subscribe"
    
    # Use a unique test email
    timestamp = int(time.time())
    test_email = f"test{timestamp}@example.com"
    
    test_data = {
        "email": test_email,
        "location": "Seattle, WA",
        "terms": True
    }
    
    print(f"🧪 Testing newsletter signup with email: {test_email}")
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Newsletter signup successful!")
            print(f"   Welcome email sent: {result.get('welcome_sent', 'Unknown')}")
            return test_email
        else:
            print("❌ Newsletter signup failed")
            return None
            
    except Exception as e:
        print(f"❌ Error testing newsletter signup: {e}")
        return None

def test_newsletter_send():
    """Test sending newsletter to all subscribers."""
    url = "https://edgefinder-czi3.onrender.com/api/newsletter/send"
    
    print("\n📧 Testing newsletter send...")
    
    try:
        response = requests.post(url, timeout=60)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Newsletter send successful!")
            print(f"   Emails sent: {result.get('emails_sent', 0)}")
            print(f"   Emails failed: {result.get('emails_failed', 0)}")
            print(f"   Total subscribers: {result.get('total_subscribers', 0)}")
        else:
            print("❌ Newsletter send failed")
            
    except Exception as e:
        print(f"❌ Error testing newsletter send: {e}")

def test_newsletter_preview():
    """Test newsletter preview to see if data generation works."""
    url = "https://edgefinder-czi3.onrender.com/api/newsletter/preview"
    
    print("\n👀 Testing newsletter preview...")
    
    try:
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Newsletter preview successful!")
            report_data = result.get('report_data', {})
            print(f"   Total games: {report_data.get('total_games', 0)}")
            print(f"   Best opportunities: {len(report_data.get('best_opportunities', []))}")
            print(f"   Most popular: {len(report_data.get('most_popular', []))}")
            print(f"   Hometown pick: {report_data.get('hometown_pick', {}).get('game', 'None')}")
        else:
            print("❌ Newsletter preview failed")
            
    except Exception as e:
        print(f"❌ Error testing newsletter preview: {e}")

def check_subscribers():
    """Check current subscribers."""
    url = "https://edgefinder-czi3.onrender.com/api/newsletter/subscribers"
    
    print("\n📊 Checking current subscribers...")
    
    try:
        response = requests.get(url, timeout=15)
        print(f"Status Code: {response.status_code}")
        
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
    print("🚀 Debugging Email System...")
    print("=" * 50)
    
    # Test newsletter signup
    test_email = test_newsletter_signup()
    
    # Test newsletter preview
    test_newsletter_preview()
    
    # Check subscribers
    check_subscribers()
    
    # Test newsletter send
    test_newsletter_send()
    
    print("\n" + "=" * 50)
    print("🔍 Debug Summary:")
    print("1. If signup works but no welcome email → Email credentials issue")
    print("2. If preview works but send fails → Email sending issue")
    print("3. If everything works but no emails received → Check spam folder")
    print("4. If timeouts occur → Website performance issue")

