#!/usr/bin/env python3
"""
Test registration API
"""
import requests
import json

def test_registration():
    """Test the registration API"""

    url = "http://localhost:8000/api/v1/auth/register"
    data = {
        "email": "test-api@example.com",
        "password": "test123",
        "full_name": "Test API User"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 201:
            print("✅ Registration successful!")
        else:
            print("❌ Registration failed")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registration()



