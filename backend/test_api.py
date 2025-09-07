#!/usr/bin/env python3
"""
Test script for the Django REST API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

def test_user_registration():
    """Test user registration"""
    print("Testing user registration...")
    
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json() if response.status_code == 201 else None

def test_user_login():
    """Test user login"""
    print("\nTesting user login...")
    
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json() if response.status_code == 200 else None

def test_get_current_user(token):
    """Test getting current user"""
    print("\nTesting get current user...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/user/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_token_refresh(refresh_token):
    """Test token refresh"""
    print("\nTesting token refresh...")
    
    data = {
        "refresh": refresh_token
    }
    
    response = requests.post(f"{BASE_URL}/refresh/", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("=== Django REST API Test ===")
    
    # Test registration
    reg_response = test_user_registration()
    
    # Test login
    login_response = test_user_login()
    
    if login_response and login_response.get('success'):
        tokens = login_response['data']
        access_token = tokens['access']
        refresh_token = tokens['refresh']
        
        # Test get current user
        test_get_current_user(access_token)
        
        # Test token refresh
        test_token_refresh(refresh_token)
    
    print("\n=== Test Complete ===")
