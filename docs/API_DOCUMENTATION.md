# Employee REST API Specification

Welcome to the official technical documentation for the **Employee REST API** (`PY-ADV-08`).

---

## 🌐 Base URL & Protocol

- **Base URL**: `http://127.0.0.1:5000`
- **Data Format**: `application/json`
- **Authentication**: Public (Unauthenticated for development)

---

## 📑 Data Models & Schemas

### Employee Resource Object

| Field | Type | Description | Validation Constraints |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Auto-incrementing Primary Key | Read-only |
| `name` | String | Employee's full name | Non-empty, max 100 chars |
| `email` | String | Unique work email address | Valid email regex, unique, max 120 chars |
| `department` | String | Organization department | Non-empty, max 80 chars |
| `role` | String | Job title / designation | Non-empty, max 80 chars |
| `salary` | Float | Annual base salary in USD | Non-negative numeric value |
| `created_at` | String (ISO 8601) | Timestamp of creation (UTC) | Read-only |
| `updated_at` | String (ISO 8601) | Timestamp of last update (UTC) | Read-only |

#### Example Employee JSON Representation:
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "department": "Engineering",
  "role": "Senior Software Engineer",
  "salary": 95000.0,
  "created_at": "2026-09-02T20:15:00+00:00",
  "updated_at": "2026-09-02T20:15:00+00:00"
}
```

---

## 🚦 Unified Response Formats

### Standard Success Response (200 OK / 201 Created)
```json
{
  "status": "success",
  "message": "Employee created successfully",
  "data": { ... }
}
```

### Standard Error Response (400 / 404 / 409 / 500)
```json
{
  "status": "error",
  "code": 400,
  "message": "Employee request validation failed",
  "errors": {
    "email": "Invalid email format. Must be e.g. user@example.com",
    "salary": "Salary must be a non-negative number"
  },
  "timestamp": "2026-09-02T20:15:00.123456+00:00"
}
```

---

## 🔗 Endpoint Reference

### 1. `POST /employees` — Create Employee

Creates a new employee record in the database.

- **Headers**:
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "department": "Engineering",
    "role": "Senior Software Engineer",
    "salary": 95000.0
  }
  ```
- **Response Headers**:
  - `Location: /employees/1`
- **Status Codes**:
  - `201 Created`: Employee successfully created.
  - `400 Bad Request`: Validation failure (missing required fields or invalid types).
  - `409 Conflict`: Email address already registered.

---

### 2. `GET /employees` — List Employees

Retrieves a paginated list of employees with support for query filters and search.

- **Query Parameters**:
  - `department` *(string, optional)*: Filter by department name (case-insensitive substring match).
  - `role` *(string, optional)*: Filter by job role.
  - `search` *(string, optional)*: Search term matching `name` or `email`.
  - `page` *(integer, default: 1)*: Page number for pagination.
  - `per_page` *(integer, default: 10, max: 100)*: Items per page.

- **Sample Request**:
  `GET /employees?department=Engineering&page=1&per_page=10`

- **Response (200 OK)**:
  ```json
  {
    "status": "success",
    "data": [
      {
        "id": 1,
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "department": "Engineering",
        "role": "Senior Software Engineer",
        "salary": 95000.0,
        "created_at": "2026-09-02T20:15:00+00:00",
        "updated_at": "2026-09-02T20:15:00+00:00"
      }
    ],
    "pagination": {
      "total": 1,
      "page": 1,
      "per_page": 10,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
  ```

---

### 3. `GET /employees/{id}` — Get Employee by ID

Retrieves a single employee by primary key ID.

- **Path Parameters**:
  - `id` *(integer, required)*: Unique employee ID.
- **Status Codes**:
  - `200 OK`: Employee found and returned.
  - `404 Not Found`: No employee exists with the given ID.

---

### 4. `PUT /employees/{id}` — Full Update Employee

Completely updates/replaces an existing employee record. Requires all employee fields.

- **Headers**:
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "name": "Jane Doe Updated",
    "email": "jane.doe.new@example.com",
    "department": "Product Engineering",
    "role": "Tech Lead",
    "salary": 110000.0
  }
  ```
- **Status Codes**:
  - `200 OK`: Record updated successfully.
  - `400 Bad Request`: Missing fields or invalid format.
  - `404 Not Found`: Employee ID does not exist.
  - `409 Conflict`: New email conflicts with another employee.

---

### 5. `PATCH /employees/{id}` — Partial Update Employee

Modifies one or more fields of an employee record while leaving unspecified fields unchanged.

- **Headers**:
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "salary": 120000.0
  }
  ```
- **Status Codes**:
  - `200 OK`: Partial update applied successfully.
  - `400 Bad Request`: Invalid payload or data type.
  - `404 Not Found`: Employee ID does not exist.

---

### 6. `DELETE /employees/{id}` — Delete Employee

Removes an employee record permanently from the database.

- **Path Parameters**:
  - `id` *(integer, required)*: Unique employee ID.
- **Status Codes**:
  - `200 OK`: Deletion confirmed with message.
  - `404 Not Found`: Employee ID does not exist.
