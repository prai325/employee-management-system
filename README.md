# Employee Management System

A FastAPI-based backend for managing employees, departments, roles, permissions, users, and attendance in an organization.

## Overview

This application provides a REST API for HR and administrative processes. It includes authentication, role-based access control, employee records, attendance tracking, and support for profile image uploads.

## Features

- User authentication with JWT
- Role and permission management
- Department management
- Employee management
- Attendance tracking and summary reports
- Pagination and search support for API listings
- Redis integration
- Email support configuration
- File upload support for profile images
- Database migrations with Alembic

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL / supported SQLAlchemy database
- Pydantic v2
- Alembic
- Redis
- JWT authentication
- Email integration

## Project Structure

```text
employee-management-system/
├── app/
│   ├── auth/
│   ├── core/
│   ├── db/
│   ├── enums/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── static/
│   ├── tasks/
│   ├── templates/
│   ├── utils/
│   ├── __init__.py
│   └── main.py
├── alembic/
├── .env
├── alembic.ini
├── requirements.txt
├── README.md
└── note.text
```

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the required configuration values.

Example:

```env
APP_NAME=Employee Management System
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/employee_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email
SMTP_PASSWORD=your_email_password
SMTP_FROM_EMAIL=your_email
SMTP_FROM_NAME=Employee Management System

REDIS_URL=redis://localhost:6379/0

AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=your_bucket
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive docs:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Main API Modules

### Authentication

- `/auth/login`
- `/auth/me`
- `/auth/admin-test`

### Roles

- `GET /roles/`
- `POST /roles/`
- `GET /roles/{role_id}`
- `PUT /roles/{role_id}`
- `DELETE /roles/{role_id}`

### Departments

- `GET /departments/`
- `POST /departments/`
- `GET /departments/{department_id}`
- `PUT /departments/{department_id}`
- `DELETE /departments/{department_id}`

### Users

- `GET /users/`
- `POST /users/`
- `GET /users/{user_id}`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

### Employees

- `GET /employees/`
- `POST /employees/`
- `GET /employees/{employee_id}`

### Attendance

- `GET /attendances/`
- `POST /attendances/`
- `GET /attendances/{attendance_id}`
- `PATCH /attendances/{attendance_id}`
- `DELETE /attendances/{attendance_id}`
- `GET /attendances/summary/{employee_id}`

## Database Migrations

This project uses Alembic for schema management.

```bash
alembic upgrade head
```

To create a new migration:

```bash
alembic revision --autogenerate -m "description"
```

## Notes

This project is intended for backend API development and is useful for real HR systems, employee records, and company attendance tracking.

## License

This project is for educational and internal business use unless a separate license is added.

## Author

You can update this section with your name, company, or team.
