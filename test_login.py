#!/usr/bin/env python3
"""
Test login endpoint
"""

import requests
import json

print('=== CHECKING SERVER STATUS ===')
try:
    # Test health endpoint
    response = requests.get('http://localhost:8000/health', timeout=5)
    print(f'Health check: {response.status_code}')
    if response.status_code == 200:
        print('[SUCCESS] Backend server is running')
    else:
        print(f'[ERROR] Health check failed: {response.status_code}')

except Exception as e:
    print(f'[ERROR] Cannot connect to backend: {e}')
    print('The backend server may not be running')

print()
print('=== TESTING LOGIN ENDPOINT ===')
url = 'http://localhost:8000/api/v1/auth/login'
data = {
    'email': 'admin@gmail.com',
    'password': 'admin123'
}

try:
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'}, timeout=10)
    print(f'Login response: {response.status_code}')
    print(f'Response: {response.text}')

    if response.status_code == 200:
        print('[SUCCESS] Login endpoint working')
    else:
        print(f'[ERROR] Login failed with status {response.status_code}')

except requests.exceptions.ConnectionError:
    print('[ERROR] Cannot connect to login endpoint - backend not running')
except Exception as e:
    print(f'[ERROR] Login error: {e}')
