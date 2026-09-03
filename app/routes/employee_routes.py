"""
Employee Resource REST API Routes implementation.
"""
import time
from flask import Blueprint, request, jsonify, current_app, url_for
from app.database import db
from app.models import Employee
from app.schemas import validate_employee_create, validate_employee_update
from app.errors import (
    ValidationError,
    ResourceNotFoundError,
    DuplicateResourceError
)

employee_bp = Blueprint('employees', __name__, url_prefix='/employees')

@employee_bp.route('', methods=['POST'])
def create_employee():
    """
    POST /employees
    Create a new employee record.
    Expects JSON payload with required fields: name, email, department, role, salary.
    Returns 201 Created on success with Location header.
    """
    if not request.is_json:
        raise ValidationError("Request Content-Type must be 'application/json'")

    data = request.get_json(silent=True)
    if data is None:
        raise ValidationError("Malformed JSON request body")

    is_valid, cleaned_data, errors = validate_employee_create(data)
    if not is_valid:
        raise ValidationError("Employee request validation failed", errors=errors)

    # Check for duplicate email
    existing_employee = Employee.query.filter_by(email=cleaned_data['email']).first()
    if existing_employee:
        raise DuplicateResourceError(
            message=f"An employee with email '{cleaned_data['email']}' already exists.",
            errors={"email": "Email address must be unique"}
        )

    new_employee = Employee(
        name=cleaned_data['name'],
        email=cleaned_data['email'],
        department=cleaned_data['department'],
        role=cleaned_data['role'],
        salary=cleaned_data['salary']
    )

    db.session.add(new_employee)
    db.session.commit()

    current_app.logger.info(f"Created new employee ID={new_employee.id}, Email={new_employee.email}")

    response = jsonify({
        "status": "success",
        "message": "Employee created successfully",
        "data": new_employee.to_dict()
    })
    response.status_code = 201
    response.headers['Location'] = f"/employees/{new_employee.id}"
    return response


@employee_bp.route('', methods=['GET'])
def get_employees():
    """
    GET /employees
    Retrieve list of employees with optional query filters and pagination.
    Query Params:
        - department (str): Filter by department name
        - role (str): Filter by job role
        - search (str): Search in employee name or email
        - page (int): Page number (default: 1)
        - per_page (int): Records per page (default: 10, max: 100)
    """
    query = Employee.query

    # Department filter
    department = request.args.get('department', type=str)
    if department:
        query = query.filter(Employee.department.ilike(f"%{department.strip()}%"))

    # Role filter
    role = request.args.get('role', type=str)
    if role:
        query = query.filter(Employee.role.ilike(f"%{role.strip()}%"))

    # Search filter (name or email)
    search = request.args.get('search', type=str)
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            (Employee.name.ilike(search_pattern)) | 
            (Employee.email.ilike(search_pattern))
        )

    # Pagination parameters
    try:
        page = max(1, request.args.get('page', default=1, type=int))
    except (ValueError, TypeError):
        page = 1

    try:
        per_page = min(100, max(1, request.args.get('per_page', default=10, type=int)))
    except (ValueError, TypeError):
        per_page = 10

    total_count = query.count()
    employees = query.order_by(Employee.id.asc()).offset((page - 1) * per_page).limit(per_page).all()

    total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1

    current_app.logger.debug(f"Retrieved {len(employees)} employees (Page {page} of {total_pages})")

    return jsonify({
        "status": "success",
        "data": [emp.to_dict() for emp in employees],
        "pagination": {
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }), 200


@employee_bp.route('/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    """
    GET /employees/{id}
    Retrieve a single employee by unique ID.
    Returns 200 OK or 404 Not Found.
    """
    employee = Employee.query.get(id)
    if not employee:
        raise ResourceNotFoundError(f"Employee with ID {id} was not found.")

    return jsonify({
        "status": "success",
        "data": employee.to_dict()
    }), 200


@employee_bp.route('/<int:id>', methods=['PUT'])
def update_employee_full(id):
    """
    PUT /employees/{id}
    Fully replace an employee record by ID. All required fields must be supplied.
    Returns 200 OK with updated employee details.
    """
    employee = Employee.query.get(id)
    if not employee:
        raise ResourceNotFoundError(f"Employee with ID {id} was not found.")

    if not request.is_json:
        raise ValidationError("Request Content-Type must be 'application/json'")

    data = request.get_json(silent=True)
    if data is None:
        raise ValidationError("Malformed JSON request body")

    is_valid, cleaned_data, errors = validate_employee_update(data, partial=False)
    if not is_valid:
        raise ValidationError("Employee update validation failed", errors=errors)

    # Email uniqueness check if email changed
    if cleaned_data['email'] != employee.email:
        existing = Employee.query.filter_by(email=cleaned_data['email']).first()
        if existing:
            raise DuplicateResourceError(
                message=f"An employee with email '{cleaned_data['email']}' already exists.",
                errors={"email": "Email address must be unique"}
            )

    # Update fields
    employee.name = cleaned_data['name']
    employee.email = cleaned_data['email']
    employee.department = cleaned_data['department']
    employee.role = cleaned_data['role']
    employee.salary = cleaned_data['salary']

    db.session.commit()

    current_app.logger.info(f"Fully updated (PUT) employee ID={id}")

    return jsonify({
        "status": "success",
        "message": "Employee updated successfully",
        "data": employee.to_dict()
    }), 200


@employee_bp.route('/<int:id>', methods=['PATCH'])
def update_employee_partial(id):
    """
    PATCH /employees/{id}
    Partially update specified fields of an employee record by ID.
    Returns 200 OK with updated employee details.
    """
    employee = Employee.query.get(id)
    if not employee:
        raise ResourceNotFoundError(f"Employee with ID {id} was not found.")

    if not request.is_json:
        raise ValidationError("Request Content-Type must be 'application/json'")

    data = request.get_json(silent=True)
    if data is None:
        raise ValidationError("Malformed JSON request body")

    is_valid, cleaned_data, errors = validate_employee_update(data, partial=True)
    if not is_valid:
        raise ValidationError("Employee partial update validation failed", errors=errors)

    # If email provided and changed, check uniqueness
    if 'email' in cleaned_data and cleaned_data['email'] != employee.email:
        existing = Employee.query.filter_by(email=cleaned_data['email']).first()
        if existing:
            raise DuplicateResourceError(
                message=f"An employee with email '{cleaned_data['email']}' already exists.",
                errors={"email": "Email address must be unique"}
            )

    # Apply partial updates
    for field, val in cleaned_data.items():
        setattr(employee, field, val)

    db.session.commit()

    current_app.logger.info(f"Partially updated (PATCH) employee ID={id}")

    return jsonify({
        "status": "success",
        "message": "Employee partially updated successfully",
        "data": employee.to_dict()
    }), 200


@employee_bp.route('/<int:id>', methods=['DELETE'])
def delete_employee(id):
    """
    DELETE /employees/{id}
    Delete an employee record by ID.
    Returns 200 OK with deletion confirmation message.
    """
    employee = Employee.query.get(id)
    if not employee:
        raise ResourceNotFoundError(f"Employee with ID {id} was not found.")

    db.session.delete(employee)
    db.session.commit()

    current_app.logger.info(f"Deleted employee ID={id}")

    return jsonify({
        "status": "success",
        "message": f"Employee with ID {id} deleted successfully."
    }), 200
