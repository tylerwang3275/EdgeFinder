#!/usr/bin/env python3
"""
Test script to verify the email system is working with the configured environment variables.
"""

import requests
import json
import time
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_website_newsletter_signup():
    """Test the newsletter signup on the deployed website."""
    print("🔍 Testing Newsletter Signup on Deployed Website...")
    
    website_url = "https://edgefinder-czi3.onrender.com"
    signup_url = f"{website_url}/api/newsletter/subscribe"
    
    # Create unique test email
    timestamp = int(time.time())
    test_data = {
        "email": f"test_{timestamp}@example.com",
        "location": "Seattle",
        "terms": True
    }
    
    print(f"📧 Testing signup with email: {test_data['email']}")
    print(f"📍 Location: {test_data['location']}")
    print(f"🌐 Signup URL: {signup_url}")
    
    try:
        # Send POST request with longer timeout
        response = requests.post(
            signup_url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # Increased timeout for email sending
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Newsletter signup successful!")
            print(f"📧 Email: {result.get('email')}")
            print(f"📬 Welcome sent: {result.get('welcome_sent', False)}")
            print(f"💬 Message: {result.get('message')}")
            
            if result.get('welcome_sent'):
                print("🎉 Welcome email was sent successfully!")
                return True
            else:
                print("⚠️ Newsletter signup worked but welcome email was not sent")
                return False
        else:
            print(f"❌ Newsletter signup failed!")
            print(f"📊 Status Code: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - this might indicate email sending is still slow")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - website may be down")
        return False
    except Exception as e:
        print(f"❌ Error testing newsletter signup: {e}")
        return False

def test_local_email_system():
    """Test the email system locally to verify it works."""
    print("\n🔍 Testing Local Email System...")
    
    try:
        from src.services.welcome_email_service import WelcomeEmailService
        
        service = WelcomeEmailService()
        print(f"✅ WelcomeEmailService created")
        print(f"📧 SMTP Server: {service.smtp_server}")
        print(f"📧 SMTP Port: {service.smtp_port}")
        print(f"📧 Sender Email: {service.sender_email}")
        print(f"📧 Sender Name: {service.sender_name}")
        
        # Check if credentials are configured
        if not service.sender_email or not service.sender_password:
            print("❌ Email credentials are not configured")
            return False
        
        print("✅ Email credentials are configured")
        
        # Test live data fetching
        print("\n🔍 Testing live data fetching...")
        live_data = service._get_live_data()
        print(f"✅ Live data fetched: {len(live_data)} sections")
        
        # Test email content generation
        print("\n🔍 Testing email content generation...")
        html_content = service._create_welcome_html("TestUser", "Seattle", live_data)
        text_content = service._create_welcome_text("TestUser", "Seattle", live_data)
        
        print(f"✅ HTML content generated: {len(html_content)} characters")
        print(f"✅ Text content generated: {len(text_content)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing local email system: {e}")
        return False

def test_newsletter_data_model():
    """Test the newsletter data model."""
    print("\n🔍 Testing Newsletter Data Model...")
    
    try:
        from src.models.newsletter import NewsletterData
        
        newsletter_data = NewsletterData()
        print("✅ NewsletterData created successfully")
        
        # Get all subscribers
        subscribers = newsletter_data.get_active_subscriptions()
        print(f"📊 Total active subscribers: {len(subscribers)}")
        
        if subscribers:
            print("📧 Recent subscribers:")
            for sub in subscribers[-3:]:  # Show last 3
                print(f"  - {sub['email']} from {sub['location']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing NewsletterData: {e}")
        return False

def main():
    """Run all email tests."""
    print("🚀 EdgeFinder Email System Verification")
    print("=" * 50)
    
    tests = [
        test_local_email_system,
        test_newsletter_data_model,
        test_website_newsletter_signup
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
            print()
    
    print("=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"  ✅ Passed: {passed}/{total}")
    print(f"  ❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All email tests passed!")
        print("💡 The newsletter signup and email system is working correctly.")
        print("📧 Users should now receive welcome emails immediately after signup!")
    else:
        print("\n⚠️ Some email tests failed.")
        print("💡 Check the error messages above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
