# JWT Authentication API (FastAPI + PostgreSQL)

A REST API built with FastAPI that demonstrates user authentication using JWT access tokens and refresh token renewal for Single Page Applications (SPAs).

This project was created to learn modern backend architecture, authentication flows, database migrations, testing, and deployment practices using Python.

**Last updated:** 14-06-2026

---

## Features

- User registration and authentication
- JWT-based access tokens
- Refresh token renewal for SPA applications
- Protected API routes
- PostgreSQL database integration (Neon)
- Database migrations with Alembic
- Swagger / OpenAPI documentation
- Clean layered architecture (routes, services, models, schemas)
- Manual authentication test suite (no external testing framework required)
- Vue 3 frontend integration for testing authentication flows

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

The project follows a layered architecture to improve maintainability and separation of concerns.

- **routes** → API endpoints (HTTP layer)
- **services** → Business logic and authentication
- **models** → SQLAlchemy database models
- **schemas** → Pydantic request/response validation
- **security** → Password hashing and JWT handling
- **db** → Database configuration and session management
- **tests** → Manual authentication verification scripts

---

## Authentication Flow

This project uses JWT authentication with refresh token renewal.

1. User logs in using username and password
2. Server validates credentials and returns:
   - JWT access token
   - Refresh token
3. Client stores both tokens
4. Access token is used for protected API requests
5. When the access token expires:
   - Client sends the refresh token to `/refresh-token-spa`
   - Server validates the refresh token
   - Server issues a new access token and refresh token
6. Client continues the session without requiring another login

**Note:** Refresh tokens are currently JWT-based and are not persisted in the database.

---

## Setup Instructions

### 1. Clone the Repository

git clone <your-repository-url>

cd <your-project-folder>

---

### 2. Create a Virtual Environment

python -m venv venv

Activate it:

**Windows (PowerShell)**

venv\Scripts\activate

---

### 3. Install Dependencies

pip install -r requirements.txt

---

### 4. Configure Environment Variables

Create a `.env` file in the project root:

DATABASE_URL=your_postgres_connection

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=2

REFRESH_TOKEN_EXPIRE_MINUTES=5

---

### 5. Run Database Migrations

Apply all existing Alembic migrations:

alembic upgrade head

**Note:** Database schema changes are managed through Alembic migrations. The application does not use SQLAlchemy's `create_all()` method.

---

### 6. Start the Server

uvicorn api.api:app --reload

API:

http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs

---

## Development: Creating New Migrations

After modifying a SQLAlchemy model:

alembic revision --autogenerate -m "describe your change"

Review the generated migration and then apply it:

alembic upgrade head

Commit both the model changes and the generated migration file to source control.

---

## Vue 3 Frontend (Testing Client)

A companion frontend is available for testing authentication flows:

https://github.com/persteenolsen/vue-fastapi-jwt-refresh-auth-client

Features:

- Login flow
- Token storage
- Protected route access
- Refresh token handling

---

## Manual Tests (Authentication Verification)

This project includes a lightweight manual test suite for verifying JWT authentication behavior without requiring pytest.

### Run Tests

python -m tests.test_auth_manual

### What Is Tested

- Valid access token authentication
- Expired token handling
- Invalid token detection
- Invalid signature detection

### Example Output

Valid token test: testuser

Expired token test: None

Invalid signature test: None

All tests finished

---

## API Endpoints

### Public Endpoints

- POST `/token` → Login and receive access token
- POST `/tokens-spa` → Login and receive access token + refresh token
- POST `/refresh-token-spa` → Obtain new tokens using refresh token

### Protected Endpoints

- GET `/users/me` → Current authenticated user
- GET `/protected-route` → Protected route example
- GET `/get-all-users` → List all users

---

## Security Notes

- Passwords are hashed before storage
- JWT tokens include expiration timestamps
- Access tokens are short-lived
- Refresh tokens allow session renewal without re-login
- Protected routes require a valid access token
- SQLAlchemy models are managed through Alembic migrations

---

## Future Improvements

- Store refresh tokens in the database
- Implement refresh token rotation and reuse detection
- Add refresh token revocation support
- Use HTTP-only cookies for refresh tokens
- Add rate limiting to authentication endpoints
- Improve logging and monitoring
- Replace manual tests with pytest
- Add CI/CD pipeline for automated testing

---

## Learning Goals

This project was built as part of a learning journey covering:

- JWT authentication
- Refresh token workflows
- FastAPI backend development
- PostgreSQL and database migrations
- Full-stack integration with Vue 3
- Software testing fundamentals
- Cloud deployment workflows

---

## Author

Built by Per Olsen

Portfolio project focused on backend development, authentication systems, and AI-related applications.