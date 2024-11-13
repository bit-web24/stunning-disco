# FastAPI JWT Authentication Application

This FastAPI application is built with JWT-based authentication and MongoDB as the database. It uses OAuth2 with a password flow, enabling secure authentication for protected routes. The API supports basic CRUD operations on users with role-based authorization.

## Features

- **User Authentication**: JWT authentication with access tokens
- **User Management**: Register, login, update, and delete user profiles
- **MongoDB Integration**: Uses MongoDB Atlas for persistent data storage
- **Swagger UI**: Automatically generated API documentation with Swagger

## Table of Contents

1. [Getting Started](#getting-started)
2. [Environment Variables](#environment-variables)
3. [Running the Application](#running-the-application)
4. [API Endpoints](#api-endpoints)
5. [Testing Authorization in Swagger](#testing-authorization-in-swagger)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB Atlas account (recommended)  or local MongoDB setup

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bit-web24/stunning-disco.git
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up MongoDB Atlas or Local Database**

   - Sign up for MongoDB Atlas and create a cluster.
   - Obtain your connection string and set it in the `.env` file (see below).

## Environment Variables

Create a `.env` file in the root directory to configure environment variables:

```plaintext
ACCESS_TOKEN_EXPIRE_MINUTES=
ALGORITHM="HS256"
JWT_SECRET_KEY=
DB_URL=
DB_NAME=
```

## Running the Application

### Locally

To start the application, run:

```bash
uvicorn app.main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.


## API Endpoints

### Authentication Endpoints

- **POST /login**: Authenticate a user and generate a JWT token.

### User Endpoints

- **POST /user/signup**: Register a new user.
- **GET /user/**: Retrieve the current user's profile.
- **PUT /user/**: Update the current user's profile.
- **DELETE /user/**: Delete the current user.

### Protected Routes

To access protected routes, include the `Authorization: Bearer <token>` header in your requests.

## Testing Authorization in Swagger

1. Start the FastAPI server and go to the Swagger UI at `http://127.0.0.1:8000/docs`.
2. Click the **Authorize** button at the top right.
3. In the **Authorize** modal, enter `username` and `password` for the `JWT (OAuth2, password)` field.
4. After successful login, the token is stored, and you can make requests to protected endpoints directly from Swagger.

## Troubleshooting

### Common Errors

- **MongoDB Connection**: Ensure your MongoDB URI is correct and accessible. Verify network permissions in MongoDB Atlas if using it.
- **JWT Token Expiry**: Check that the `ACCESS_TOKEN_EXPIRE_MINUTES` is set correctly. Adjust the value if tokens are expiring too quickly.
- **Swagger Token Authorization Issue**: If the token is not showing in Swagger, manually enter it in the **Authorize** modal.
