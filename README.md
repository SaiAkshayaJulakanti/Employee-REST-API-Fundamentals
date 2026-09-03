# 🚀 Employee REST API — Flask API Development Fundamentals (PY-ADV-08)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)](https://www.sqlalchemy.org/)
[![Database](https://img.shields.io/badge/database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-orange.svg)](https://docs.pytest.org/)

A complete, production-grade **Employee REST API** built with Flask, Flask-SQLAlchemy, and SQLite database. Designed as part of **PY-ADV-08 — REST API Development Fundamentals**, this project demonstrates REST architectural principles, HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), HTTP status codes, structured JSON request validation, centralized exception handling, application logging, automated pytest suites, and Postman API testing collection.

---

## 📁 Clean & Modular Architecture

```text
employee_rest_api/
├── app/
│   ├── __init__.py           # Application Factory (create_app), middleware & logger setup
│   ├── config.py             # Configuration classes (Dev, Test, Prod)
│   ├── database.py           # SQLAlchemy database instance
│   ├── models.py             # Employee ORM Model with validation rules & serialization
│   ├── schemas.py            # Input payload validators & regex sanitizers
│   ├── errors.py             # Custom exceptions & standardized JSON error handlers
│   ├── routes/
│   │   ├── __init__.py
│   │   └── employee_routes.py # CRUD REST endpoints (POST, GET, GET/id, PUT, PATCH, DELETE)
│   └── utils/
│       ├── __init__.py
│       └── logger.py         # Formatted file (logs/app.log) & console logging setup
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures (Flask test client & SQLite memory DB)
│   ├── test_employees.py     # Complete test suite covering all routes & edge cases
│   └── run_tests.py          # Standalone Python test runner script
├── docs/
│   ├── API_DOCUMENTATION.md  # Detailed API Specification (Schemas, Headers, Codes)
│   └── REST_FUNDAMENTALS.md  # Theoretical guide on REST principles & HTTP verbs
├── postman/
│   └── Employee_REST_API.postman_collection.json # Exported Postman Collection v2.1
├── logs/                     # Auto-created log directory (app.log)
├── app.py                    # Server startup script
├── requirements.txt          # Project dependencies
└── README.md                 # Master project documentation
```

---

## ⚡ REST Endpoints Overview

| HTTP Method | Resource URI | Description | Success Status | Request Body |
| :--- | :--- | :--- | :---: | :---: |
| `POST` | `/employees` | Create a new employee | `201 Created` | Required (Full JSON) |
| `GET` | `/employees` | List employees (filters & pagination) | `200 OK` | None |
| `GET` | `/employees/{id}` | Retrieve employee by ID | `200 OK` | None |
| `PUT` | `/employees/{id}` | Full update/replacement of employee | `200 OK` | Required (Full JSON) |
| `PATCH` | `/employees/{id}` | Partial update of employee fields | `200 OK` | Required (Partial JSON) |
| `DELETE` | `/employees/{id}` | Delete employee by ID | `200 OK` | None |
| `GET` | `/health` | API health check endpoint | `200 OK` | None |

---

## 🛠️ Setup & Execution Instructions

### 1. Prerequisites
- Python 3.8 or higher installed.

### 2. Install Dependencies
Navigate to project directory and install required Python packages:

```bash
cd employee_rest_api
pip install -r requirements.txt
```

### 3. Run the Flask API Server
Start the development server:

```bash
python app.py
```

The API will start at: `http://127.0.0.1:5000`

---

## 🧪 Running Automated Tests

Run the full pytest suite using the included standalone test runner:

```bash
python tests/run_tests.py
```

Or run directly via pytest:

```bash
pytest tests/ -v
```

### Test Coverage Highlights:
- ✅ Health check & Root API info endpoints.
- ✅ Successful Employee creation (`201 Created`) & `Location` header validation.
- ✅ Missing field validation (`400 Bad Request`).
- ✅ Invalid email & negative salary validation (`400 Bad Request`).
- ✅ Duplicate email uniqueness constraint (`409 Conflict`).
- ✅ Non-JSON media type error (`415` / `400`).
- ✅ List employees with department filter & search (`200 OK`).
- ✅ Fetch employee by ID (`200 OK`) and non-existent ID (`404 Not Found`).
- ✅ Full update (`PUT`) & Partial update (`PATCH`).
- ✅ Employee deletion (`200 OK`) & subsequent `404` verification.
- ✅ Invalid route method (`405 Method Not Allowed`).

---

## 📮 Testing with Postman

1. Open **Postman**.
2. Click **Import** -> **File** -> Select `postman/Employee_REST_API.postman_collection.json`.
3. The collection imports 10 pre-configured API requests complete with pre-written test assertions (`pm.test(...)`).
4. Ensure the Flask server is running (`python app.py`) and click **Run Collection**.

---

## 📖 Theoretical Documentation

- For deep architectural concepts, HTTP verb idempotency matrix, and HTTP status code reference, read: [REST_FUNDAMENTALS.md](file:///c:/Users/HAI/OneDrive/Desktop/Vibe%20Coding%20Assignment/employee_rest_api/docs/REST_FUNDAMENTALS.md).
- For complete payload samples and JSON schemas, read: [API_DOCUMENTATION.md](file:///c:/Users/HAI/OneDrive/Desktop/Vibe%20Coding%20Assignment/employee_rest_api/docs/API_DOCUMENTATION.md).
