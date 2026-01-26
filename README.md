# Python + FastAPI + PostgreSQL + Authentication by JWT with Refresh Tokens + Alembic + SQLAlchemy

A REST API that serves Authentication by JWT with Refresh Tokens + Registration

Last updated:

- 26-01-2026

Python Version:

- 3.12

# Get startet

- Clone the repository from my GitHub 

- Create a virtual environment by Powershell or VS Code:

"python -m venv <name_of_venv>"

- Go to the virtual environment's directory and activate it:

"cd venv"

"Scripts/activate"

- Install the requirements:

"cd ../"

"pip3 install -r requirements.txt"

# Swagger documentation / Testing the API

FastAPI provides the Swagger documentation of the API where you can perform CRUD operations

To access the documentation, we must run uvicorn:

"uvicorn main:app --reload"

If everything works fine, the FastAPI and Swagger documentation is now available at: 

`http://127.0.0.1:8000/docs`

- Use the Swagger for Register a User in the PostgreSQL DB and try to perform Login operations

- You can go to the PostgreSQL at Neon to test your data in the DB

When you make a change to the models and start run the Web App the PostgreSQL should be updated

# Authentication by JWT + Refresh Tokens

- The JWT Access Token will expire after 2 minutes and the JWT Refresh Token after 5 minuttes for testing and demo. A 401 status will happen after expiration

# The structure of the API by folders for scalability

- The Database functionality is placed in files inside the directory db

- The User Routes are placed in files inside the directory routes/user.py

- The simple Routes are placed in files inside the directory routes/simple.py

- The Models are placed in files inside the directory models

- The Schemas are placed in files inside the directory schemas

- The functionality of authentication is placed inside the directory security

- The functionality like get current user, called from the Routes, is placed inside the directory services

# Migration with Alembic

- Install and use Alembic for Migration and run:

- alembic init alembic

- For demonstration I added name in the User Model and Schema and generated and applied migration:

- alembic revision --autogenerate -m "create column name"

- alembic upgrade head

- Then run the FastAPI again and check that everything works fine

# Deployment to Vercel

- Take a look at the file "vercel.json"

- Create a Project at Vercel from your repository at GitHub with the code of this FastAPI

- Create the envirement variables from .env at Vercel with the connection to PostgreSQL

- Make a commit to your GitHub

- Go to Vercel and check that the build and deployment happened and your site is in Production

# Tech used for the Web API

- Python FastAPI
- PostgreSQL with tables for Users and RefreshTokens (For future versions with Refresh token rotations)
- OpenAPI / Swagger
- Serves Authentication by JWT with Refresh Tokens
- Hosted at Vercel Cloud using Serverless Functions

# Things to consider for future versions

- Set the minuttes for the JWT Access Tokens to 15 in .env

- Set the minuttes for the JWT Refresh Tokens to 7 DAYS in .env

- Implement Refresh token rotation

- Implement Revoked token reuse detection

- Protect the API Routes by Rate limits

The FastAPI + Vue 3 SPA were made in a simple way for showing the Authentication flow by JWT and Refresh Tokens

Happy use of FastAPI :-)

