# JWT Authentication API (FastAPI + PostgreSQL)

A REST API built with FastAPI that demonstrates user authentication using JWT access tokens and refresh token-based session renewal for SPA applications.

This project was created to learn modern backend architecture, authentication flows, testing, and deployment practices using Python.

Last updated: 13-06-2026

---

## Features

- User registration and authentication
- JWT-based access tokens
- Refresh token-based session renewal (SPA flow)
- Token type separation (`access` / `refresh`)
- Protected API routes
- PostgreSQL database integration (Neon)
- Database migrations with Alembic
- Swagger / OpenAPI documentation
- Clean layered architecture (routes, services, models, schemas)
- Manual authentication test suite (no external testing framework required)
- Vue 3 frontend integration for testing authentication flow

---

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL (Neon)
- SQLAlchemy
- Alembic
- PyJWT
- Pydantic
- Vue 3 (frontend client)

---

## Project Architecture

The project follows a layered architecture to improve scalability and maintainability:

- routes → API endpoints (HTTP layer)
- services → Business logic (authentication, user handling)
- models → Database models (SQLAlchemy)
- schemas → Request/response validation (Pydantic)
- security → Password hashing and JWT handling
- db → Database configuration and session handling
- tests → Manual authentication verification scripts

---

## Authentication Flow

This project uses JWT authentication with refresh token renewal:

1. User logs in with username and password
2. Server validates credentials and returns:
   - Short-lived JWT access token (`type: access`)
   - Refresh token (`type: refresh`)
3. Client stores tokens and uses access token for API requests
4. Access tokens are validated against:
   - Signature
   - Expiration
   - Token type (`access`)
5. When access token expires:
   - Client sends refresh token to /refresh-token-spa
   - Server validates refresh token (`type: refresh`)
   - Server issues a new access token and refresh token
6. Client continues session without requiring login

Note: This project uses refresh token renewal (not full rotation with revocation tracking).

---

## Setup Instructions

### 1. Clone repository

git clone <your-repo-url>
cd <your-project-folder>

---

### 2. Create virtual environment

python -m venv venv

Activate it:

Windows (PowerShell):
venv\Scripts\activate

---

### 3. Install dependencies

pip install -r requirements.txt

---

### 4. Configure environment variables

Create a .env file:

DATABASE_URL=your_postgres_connection
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=2
REFRESH_TOKEN_EXPIRE_MINUTES=5

---

### 5. Run database migrations

alembic upgrade head

---

### 6. Start the server

uvicorn main:app --reload

API will be available at:
http://127.0.0.1:8000

Swagger UI:
http://127.0.0.1:8000/docs

---

## Vue 3 Frontend (Testing Client)

A companion frontend is available for testing authentication flows:

https://github.com/persteenolsen/vue-fastapi-jwt-refresh-auth-client

It demonstrates:
- Login flow
- Token storage
- API authentication
- Refresh token handling

---

## Manual Tests (Authentication Verification)

This project includes a lightweight manual test suite for JWT authentication logic (no pytest required).

### Run all tests

python -m tests.test_auth_manual

### What is tested

- Valid access token authentication
- Token type validation (`access` vs `refresh`)
- Expired token handling
- Invalid signature detection

### Example output

Valid token test: testuser  
Wrong type test: None  
Token has expired!  
Expired token test: None  
Invalid token!  
Invalid signature test: None  

All tests finished

---

## API Endpoints

Public:
- POST /token → Login (JWT access token)
- POST /tokens-spa → Login (access + refresh tokens)
- POST /refresh-token-spa → Refresh session

Protected:
- GET /users/me → Get current user
- GET /protected-route → Test protected access
- GET /get-all-users → List users

---

## Security Notes

- Passwords are hashed before storage
- JWT tokens include explicit `type` claim (`access` / `refresh`)
- Access tokens are validated against type to prevent misuse
- Tokens are time-limited
- Refresh tokens extend session without re-login
- Protected routes require valid access token only

---

## Future Improvements

- Store refresh tokens in database for revocation tracking
- Implement refresh token reuse detection
- Use HTTP-only cookies for refresh tokens
- Add rate limiting on authentication endpoints
- Improve logging and monitoring
- Replace manual tests with pytest-based test suite
- Add CI/CD pipeline for automated testing

---

## Learning Purpose

This project was built as part of a learning path exploring:

- HTTP authentication → JWT → refresh token systems
- Backend architecture with FastAPI
- Full-stack integration with Vue 3
- Database design and migrations
- Software testing fundamentals
- Cloud deployment workflows

---

## Author

Built by Per Olsen  
Portfolio project for backend development and AI-related applications