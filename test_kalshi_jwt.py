#!/usr/bin/env python3
"""
Test script for Kalshi JWT authentication.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_kalshi_jwt():
    """Test Kalshi JWT authentication."""
    api_key_id = "f178b0a4-438a-47e2-b01b-25c357e48c5c"
    private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAuxEifsJZu8uTh4Rvj5ETl5pfj7dDhOwLZ55z4R3mWu6jI0UH
RAgy26w/GMpyuG2T2MlMKeed+CGvHhYPadRUx1TmdHBIFEe7tyRDbTs/FTWvfHx/
nVrpjLthfP/H+cuARvx7+DNqnFBw0KVbkKHsiu6FMWGzSWWPhYqEO6xAWBfEi55S
NcEBX1dgS1Q6RTIjuu9a3guJ/T6cWVe9UcUVlq34srOKWkYdQndkhYLeXNdEX8O5
370l/AcSRNoB92lo9avvq50B1gvc05M1A0yoBBbuh+y96z6EKtrKg8QlcgXiBLmB
BdB4Ytge0ginhENcbinq5IAend5Vv/gq1r9eKwIDAQABAoIBAF9JmB+nkhvl0+1Y
2Zbw2GEGAp1rRZpkvl52ySInn9o76p+hntTZtEZPlAhlv1AQiRoJV6GU2NO3HMOf
ixRmUxUCOy2esCicbZMZhrsSTczY/t3TcRHPaF4GaN9KTyv/rAT8wY0pa6naE81E
HcMrqBkQ7Im98Zx2fkgQydC3qkL0YGQJVXzLsOcYbW46/1EkbwWdN5cxcuN6vZbd
19iXCnnjgYrlhPxM1Dkt6419FIxJaqYTzG06X631JQElC06WGmXE3OM1Vw38k+1O
oLHwt8UsD3bLbopr1GWjZKHgQVzXGFFPi9VjDlghFwDW1lwAR42yfjYDxKDxAX0N
sz3edvECgYEAxk5mvH/T4Q4o5Rx+gsRg3gwrwiZj/Tgth4EZMWbUbFNOZFTVePHl
X8zXREw0pE4A6EKAqD/yCWcJche3HF3ze+cre+pHWMc21bxeZ+6wLs0ipRvlv+kw
bnZYEDUfFdVgGyDm04Fdl/eqUplG7JK6ly2/QVDRnFjxLpViXq4tlRMCgYEA8X2k
lu3QP6r6YHnWfquaM/Hklc7QM0sdwc4C2VIs39Nbz5xpcAQsjyA6JrdLnoNyKaiy
PH3G8sU4QJHqlUQs4BMhr8LhxVhE66dDikKHCM1IWEbxYS3c3JIWiZYxhEncnxBc
8uFQ5jT/QZMOMSvPflcrQG3eO66n4xt4DIBI7YkCgYA/QXkB/eBvNJ4U3y73tX6U
tdsrdiWE+2uCgsqveHagCz7BQFJL3xVkpqmwDoLoOj2N2NDDWopxN13K+Aef09Q8
HLRBNa0Gg51ZNloC2x91/ldjxW9W9SJOyg8zNE6zHzolzSv0IZriQ80fxebaxb8h
RCVyxz3lmnVsf5g+TV8a4wKBgQCi+o7IJbu0HGpaDiBK4PlzMT96M1ekJn/wul6F
2MXcUULXPNKT/N0twyw70NzCICg+IVIZLTHFyoCKY3AUSSyYFZFYk4fXrhjlib81
YmzL7e9zVH23fkJewmFfffPxOgAhgeOZL6NvmjjjQqIDYXPp6l6QXxXq5Zb82R8O
IM4XMQKBgB9LP14ukqB+LmKNJEqOks+0MJOITPf5swh/hZKKxPm6lpIyLbaYqnAb
DV94L3EfcdMmDe0KEuGCdSo9+RNCeSAbhsQa8gjhS8ZV+8sYf2exnLTFNS9bgyWS
Pn9qglHT+2QbE7uGWDZkf2acgvisdqwe/M21VmcK4W6cV0hum5b8
-----END RSA PRIVATE KEY-----"""
    
    print("🔍 Testing Kalshi JWT Authentication:")
    print(f"API Key ID: {api_key_id[:8]}...")
    print(f"Private Key: {'✅ Set' if private_key else '❌ Missing'}")
    
    try:
        from src.auth.kalshi_auth import KalshiAuth
        
        # Initialize authentication
        auth = KalshiAuth(api_key_id, private_key)
        print("✅ JWT authentication initialized successfully")
        
        # Generate token
        token = auth.get_auth_token()
        print(f"✅ JWT token generated: {token[:50]}...")
        
        # Get headers
        headers = auth.get_auth_headers()
        print(f"✅ Auth headers: {headers}")
        
        # Test API connection
        import requests
        url = "https://api.elections.kalshi.com/events"
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📊 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Successfully connected to Kalshi API!")
            data = response.json()
            print(f"📈 Response data: {str(data)[:200]}...")
        else:
            print(f"⚠️  API Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_kalshi_jwt()
