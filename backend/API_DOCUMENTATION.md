# BikeGPS Tracker - Django REST API Documentation

This document describes the Django REST Framework API endpoints for the BikeGPS Tracker backend.

## Base URL
```
http://localhost:8000/api/auth
```

## Authentication
All API endpoints (except authentication) require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Response Format
All API responses follow this format:
```json
{
  "success": true,
  "message": "Optional message",
  "data": <response_data>
}
```

## Error Response Format
```json
{
  "success": false,
  "message": "Error message",
  "error": "Detailed error information"
}
```

---

## Authentication Endpoints

### User Registration
**POST** `/api/auth/register/`

Register a new user account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "password_confirm": "string",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "access": "jwt-access-token",
    "refresh": "jwt-refresh-token",
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "first_name": "Test",
      "last_name": "User",
      "date_joined": "2024-01-01T12:00:00Z"
    }
  }
}
```

### User Login
**POST** `/api/auth/login/`

Authenticate user with username and password.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access": "jwt-access-token",
    "refresh": "jwt-refresh-token",
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "first_name": "Test",
      "last_name": "User",
      "date_joined": "2024-01-01T12:00:00Z"
    }
  }
}
```

### User Logout
**POST** `/api/auth/logout/`

Logout user and blacklist refresh token.

**Request Body:**
```json
{
  "refresh_token": "jwt-refresh-token"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

### Token Refresh
**POST** `/api/auth/refresh/`

Refresh expired access token using refresh token.

**Request Body:**
```json
{
  "refresh": "jwt-refresh-token"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "access": "new-jwt-access-token"
  }
}
```

### Get Current User
**GET** `/api/auth/user/`

Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <jwt-access-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "date_joined": "2024-01-01T12:00:00Z"
  }
}
```

### Update User Profile
**GET/PUT/PATCH** `/api/auth/profile/`

Get or update user profile information.

**Headers:**
```
Authorization: Bearer <jwt-access-token>
```

**GET Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "date_joined": "2024-01-01T12:00:00Z"
  }
}
```

**PUT/PATCH Request Body:**
```json
{
  "email": "newemail@example.com",
  "first_name": "New First Name",
  "last_name": "New Last Name"
}
```

---

## JWT Token Configuration

### Access Token
- **Lifetime**: 60 minutes
- **Algorithm**: HS256
- **Usage**: Include in Authorization header for API requests

### Refresh Token
- **Lifetime**: 7 days
- **Usage**: Use to get new access tokens when expired
- **Rotation**: Enabled (new refresh token issued on refresh)

### Token Claims
```json
{
  "user_id": 1,
  "exp": 1640995200,
  "iat": 1640991600,
  "token_type": "access",
  "jti": "unique-token-id"
}
```

---

## Error Codes

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

### Common Error Responses

**400 Bad Request:**
```json
{
  "success": false,
  "message": "Invalid credentials",
  "error": {
    "non_field_errors": ["Invalid credentials"]
  }
}
```

**401 Unauthorized:**
```json
{
  "success": false,
  "message": "Authentication credentials were not provided.",
  "error": "Authentication credentials were not provided."
}
```

**422 Validation Error:**
```json
{
  "success": false,
  "message": "Validation failed",
  "error": {
    "password": ["This field is required."],
    "email": ["Enter a valid email address."]
  }
}
```

---

## Testing the API

### Using cURL

**Register a new user:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**Get current user:**
```bash
curl -X GET http://localhost:8000/api/auth/user/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using Python requests

```python
import requests

# Register
response = requests.post('http://localhost:8000/api/auth/register/', json={
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'testpass123',
    'password_confirm': 'testpass123'
})

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'username': 'testuser',
    'password': 'testpass123'
})

tokens = response.json()['data']
access_token = tokens['access']

# Get current user
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get('http://localhost:8000/api/auth/user/', headers=headers)
```

---

## Django Admin

Access the Django admin interface at:
```
http://localhost:8000/admin/
```

**Default superuser:**
- Username: `admin`
- Password: `admin123`

---

## CORS Configuration

The API is configured to allow requests from:
- `http://localhost:3000` (React development)
- `http://127.0.0.1:3000`
- `http://localhost:8081` (Expo development)
- `http://127.0.0.1:8081`
- `exp://192.168.131.234:8081` (Expo development server)

For development, all origins are allowed. In production, configure specific allowed origins.

---

## Security Features

### Password Validation
- Minimum 8 characters
- Cannot be too similar to user information
- Cannot be a common password
- Cannot be entirely numeric

### JWT Security
- Tokens are signed with Django's SECRET_KEY
- Access tokens expire after 60 minutes
- Refresh tokens expire after 7 days
- Token rotation is enabled
- Blacklisted tokens are invalidated

### CORS Protection
- Configured for specific origins
- Credentials are allowed for authenticated requests
- Proper headers are configured

---

## Development Setup

### Prerequisites
- Python 3.8+
- Django 5.2.6
- Django REST Framework 3.15.2
- djangorestframework-simplejwt 5.3.0

### Installation
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Environment Variables
Set the following in your environment or Django settings:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Configure for production

---

## Production Considerations

### Security
- Change the default SECRET_KEY
- Set DEBUG=False
- Configure proper ALLOWED_HOSTS
- Use HTTPS in production
- Configure proper CORS origins
- Use environment variables for sensitive data

### Performance
- Use a production database (PostgreSQL recommended)
- Configure caching (Redis recommended)
- Use a production WSGI server (Gunicorn)
- Set up static file serving
- Configure logging

### Monitoring
- Set up error tracking (Sentry)
- Configure logging
- Monitor API performance
- Set up health checks

---

**API Version:** 1.0  
**Last Updated:** January 2024

---

## IoT GPS Endpoints

Base path: `/api/iot/`

### List GPS Data
- Method: `GET`
- URL: `/api/iot/gps/`
- Response: `200 OK`
```json
[
  {
    "id": 1,
    "device_id": "device-123",
    "latitude": 37.422,
    "longitude": -122.084,
    "timestamp": "2025-01-01T12:34:56Z"
  }
]
```

### Create GPS Data
- Method: `POST`
- URL: `/api/iot/gps/`
- Body (JSON):
```json
{
  "device_id": "device-123",
  "latitude": 37.422,
  "longitude": -122.084
}
```
- Response: `201 Created`
```json
{
  "id": 2,
  "device_id": "device-123",
  "latitude": 37.422,
  "longitude": -122.084,
  "timestamp": "2025-01-01T12:35:01Z"
}
```

### Retrieve GPS Data
- Method: `GET`
- URL: `/api/iot/gps/{id}/`
- Response: `200 OK`

### Update GPS Data
- Method: `PUT`
- URL: `/api/iot/gps/{id}/`
- Body (JSON): same as create
- Response: `200 OK`

### Delete GPS Data
- Method: `DELETE`
- URL: `/api/iot/gps/{id}/`
- Response: `204 No Content`

### Notes
- `timestamp` is read-only and set by the server.
- All responses are JSON.
