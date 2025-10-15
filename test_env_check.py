#!/usr/bin/env python3
"""
Test script to check if environment variables are properly configured on Render.
"""

import requests
import json

def test_environment_variables():
    """Test if we can check environment variables on the deployed site."""
    print("🔍 Testing Environment Variables on Deployed Website...")
    
    # First, let's try to access a simple endpoint to see if the site is responsive
    website_url = "https://edgefinder-czi3.onrender.com"
    
    try:
        # Test basic connectivity
        response = requests.get(website_url, timeout=10)
        print(f"📊 Website Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Website is accessible")
        else:
            print(f"❌ Website returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing website: {e}")
        return False
    
    # Now let's try a simple newsletter signup with a very short timeout
    # to see if we get a different error
    signup_url = f"{website_url}/api/newsletter/subscribe"
    test_data = {
        "email": "quicktest@example.com",
        "location": "Seattle", 
        "terms": True
    }
    
    print(f"\n🔍 Testing newsletter signup with short timeout...")
    
    try:
        response = requests.post(
            signup_url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=5  # Very short timeout to see what happens
        )
        
        print(f"📊 Response Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Newsletter signup successful!")
            print(f"📧 Welcome sent: {result.get('welcome_sent', False)}")
            return True
        else:
            print(f"❌ Newsletter signup failed with status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 5 seconds")
        print("💡 This suggests the email sending process is hanging")
        print("💡 The environment variables might not be properly configured")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run the environment test."""
    print("🚀 EdgeFinder Environment Variables Test")
    print("=" * 50)
    
    success = test_environment_variables()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Environment variables appear to be working!")
        print("💡 The newsletter signup and email system should be functional.")
    else:
        print("❌ Environment variables may not be properly configured.")
        print("💡 Please double-check your Render environment variables:")
        print("   - SMTP_SERVER=smtp.gmail.com")
        print("   - SMTP_PORT=587") 
        print("   - SENDER_EMAIL=edgefindernews@gmail.com")
        print("   - SENDER_PASSWORD=ufzn fneg awxz jivh")
        print("   - SENDER_NAME=EdgeFinder")
        print("💡 Make sure to save and redeploy after adding them.")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
