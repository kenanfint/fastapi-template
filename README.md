# Python FastAPI Template

A clean, modular, and scalable FastAPI project template using SQLAlchemy ORM and Pydantic schemas.

---

## 🚀 About this project

This template is designed to help you quickly start building RESTful APIs with Python FastAPI. It includes:

- Modular folder structure for scalability
- SQLAlchemy ORM for database modeling
- Pydantic schemas for data validation and serialization
- Versioned API routes (`/api/v1`)
- Configuration management using environment variables
- Dependency injection for database sessions
- Ready for extension with new entities and features
- Modern packaging using Poetry
- Optional Docker support for easy deployment

---

## 📦 Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/kenanfint/fastapi-template.git
```

### 2. (Optional) Rename your project

If you'd like a different project name, rename the folder:

```bash
mv fastapi-template `your-project-name`
cd `your-project-name`
```

### 3. Remove the existing git history

```bash
rm -rf .git
```

### 4. Create a `.env` file

A `.env.example` file is provided. Simply rename it:

```bash
mv .env.example .env
```

The `.env` should look like this:

```
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key_here
```

---

## 🛠️ Running Locally (Poetry)

This template uses **Poetry** for modern Python dependency management.

### Install Poetry

If you don't have Poetry installed yet:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Install dependencies

```bash
poetry install
```

### Run the application

```bash
poetry run uvicorn app.main:app --reload
```

Open your browser at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🐳 Running with Docker (Optional)

Make sure you have Docker installed, then run:

```bash
docker build -t fastapi-template .
docker run -it --rm -p 8000:8000 fastapi-template
```

Your API will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧱 Project Structure

```
python_fast_api_template/
├── app/
│   ├── api/            # API route definitions, versioned (e.g., v1)
│   ├── core/           # Configuration, settings, security
│   ├── crud/           # Database CRUD operation functions
│   ├── db/             # Database setup, models, sessions
│   ├── schemas/        # Pydantic models (request/response schemas)
│   ├── services/       # Business logic and validation layer
│   ├── utils/          # Utility functions/helpers
│   └── main.py         # Application entrypoint
├── .env.example        # Example environment variables
├── .gitignore          # Git ignore rules
├── pyproject.toml      # Poetry project definition
├── Dockerfile          # Docker container specification
└── README.md           # This file
```

---

## ✨ How to create a new resource (e.g., `users`)

### 1. Create your database model

`app/db/models/user.py`:

```python
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

### 2. Create Pydantic schemas

`app/schemas/user.py`:

```python
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
```

### 3. Implement CRUD

`app/crud/user.py`:

```python
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

### 4. Add business logic (optional)

`app/services/user_service.py`:

```python
from sqlalchemy.orm import Session
from app import crud
from app.schemas import user as user_schema

def create_user(db: Session, user_in: user_schema.UserCreate):
    existing = crud.user.get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("Email already registered")
    return crud.user.create_user(db, user_in)
```

### 5. Create API routes

`app/api/v1/routes_users.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.services import user_service
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=user_schema.UserRead)
def create_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### 6. Register the route

In `app/main.py`:

```python
from fastapi import FastAPI
from app.api.v1 import routes_users

app = FastAPI()

app.include_router(routes_users.router, prefix="/api/v1", tags=["users"])
```

---

## 🤝 Contributing

Feel free to open issues or pull requests to improve this template.

---

## 📄 License

MIT License © Kenan Fintelman
