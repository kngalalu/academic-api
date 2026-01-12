## Installation Requirements

- Python 3.11
- FastAPI
- SQLModel
- SQLite (default)
- OAuth2 + JWT authentication
- Passlib (bcrypt)
- python-dotenv

## Setup Instructions

### 1. Clone the repository

### 2. Create and activate a virtual environment

#### Windows

python -m venv venv
venv\Scripts\activate

#### macOS / Linux

python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Environment variables

Create a `.env` file in the project root:

Add : 
SECRET_KEY=your-super-secret-key

Generate a secure key can try using:

openssl rand -hex 32

### 5. Run the application

Command : uvicorn main:app --reload or 


The API will be available at:

http://127.0.0.1:8000

Swagger UI:
http://127.0.0.1:8000/docs

## Authentication

The API uses OAuth2 password flow.

1. Use `/login/access-token` to obtain a JWT token
2. Authorize in Swagger UI using:
3. Access authenticated endpoints
