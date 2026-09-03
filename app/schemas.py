"""
Request Data Validation and Sanitization Schemas.
"""
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_employee_create(data):
    """
    Validate JSON payload for creating an Employee (POST) or replacing an Employee (PUT).
    
    Returns:
        tuple: (is_valid: bool, cleaned_data: dict, errors: dict)
    """
    errors = {}
    cleaned = {}

    if not isinstance(data, dict):
        return False, {}, {"payload": "Request body must be a valid JSON object"}

    required_fields = ['name', 'email', 'department', 'role', 'salary']
    for field in required_fields:
        if field not in data or data[field] is None:
            errors[field] = f"Field '{field}' is required and cannot be null"

    # If missing required fields, return early with errors
    if errors:
        return False, {}, errors

    # Validate Name
    name = str(data.get('name', '')).strip()
    if not name:
        errors['name'] = "Name cannot be empty or blank"
    elif len(name) > 100:
        errors['name'] = "Name cannot exceed 100 characters"
    else:
        cleaned['name'] = name

    # Validate Email
    email = str(data.get('email', '')).strip().lower()
    if not email:
        errors['email'] = "Email cannot be empty"
    elif not EMAIL_REGEX.match(email):
        errors['email'] = "Invalid email format. Must be e.g. user@example.com"
    elif len(email) > 120:
        errors['email'] = "Email cannot exceed 120 characters"
    else:
        cleaned['email'] = email

    # Validate Department
    department = str(data.get('department', '')).strip()
    if not department:
        errors['department'] = "Department cannot be empty"
    elif len(department) > 80:
        errors['department'] = "Department cannot exceed 80 characters"
    else:
        cleaned['department'] = department

    # Validate Role
    role = str(data.get('role', '')).strip()
    if not role:
        errors['role'] = "Role cannot be empty"
    elif len(role) > 80:
        errors['role'] = "Role cannot exceed 80 characters"
    else:
        cleaned['role'] = role

    # Validate Salary
    salary = data.get('salary')
    try:
        salary_val = float(salary)
        if salary_val < 0:
            errors['salary'] = "Salary must be a non-negative number"
        else:
            cleaned['salary'] = salary_val
    except (ValueError, TypeError):
        errors['salary'] = "Salary must be a valid numeric value"

    is_valid = len(errors) == 0
    return is_valid, cleaned if is_valid else {}, errors


def validate_employee_update(data, partial=False):
    """
    Validate JSON payload for updating an Employee.
    If partial=True (PATCH), fields are optional but validated if provided.
    If partial=False (PUT), requires all fields via validate_employee_create.
    
    Returns:
        tuple: (is_valid: bool, cleaned_data: dict, errors: dict)
    """
    if not partial:
        return validate_employee_create(data)

    errors = {}
    cleaned = {}

    if not isinstance(data, dict):
        return False, {}, {"payload": "Request body must be a valid JSON object"}

    if not data:
        return False, {}, {"payload": "At least one field must be provided for partial update (PATCH)"}

    # Validate Name if present
    if 'name' in data:
        if data['name'] is None:
            errors['name'] = "Name cannot be null"
        else:
            name = str(data['name']).strip()
            if not name:
                errors['name'] = "Name cannot be empty or blank"
            elif len(name) > 100:
                errors['name'] = "Name cannot exceed 100 characters"
            else:
                cleaned['name'] = name

    # Validate Email if present
    if 'email' in data:
        if data['email'] is None:
            errors['email'] = "Email cannot be null"
        else:
            email = str(data['email']).strip().lower()
            if not email:
                errors['email'] = "Email cannot be empty"
            elif not EMAIL_REGEX.match(email):
                errors['email'] = "Invalid email format. Must be e.g. user@example.com"
            elif len(email) > 120:
                errors['email'] = "Email cannot exceed 120 characters"
            else:
                cleaned['email'] = email

    # Validate Department if present
    if 'department' in data:
        if data['department'] is None:
            errors['department'] = "Department cannot be null"
        else:
            department = str(data['department']).strip()
            if not department:
                errors['department'] = "Department cannot be empty"
            elif len(department) > 80:
                errors['department'] = "Department cannot exceed 80 characters"
            else:
                cleaned['department'] = department

    # Validate Role if present
    if 'role' in data:
        if data['role'] is None:
            errors['role'] = "Role cannot be null"
        else:
            role = str(data['role']).strip()
            if not role:
                errors['role'] = "Role cannot be empty"
            elif len(role) > 80:
                errors['role'] = "Role cannot exceed 80 characters"
            else:
                cleaned['role'] = role

    # Validate Salary if present
    if 'salary' in data:
        if data['salary'] is None:
            errors['salary'] = "Salary cannot be null"
        else:
            salary = data['salary']
            try:
                salary_val = float(salary)
                if salary_val < 0:
                    errors['salary'] = "Salary must be a non-negative number"
                else:
                    cleaned['salary'] = salary_val
            except (ValueError, TypeError):
                errors['salary'] = "Salary must be a valid numeric value"

    is_valid = len(errors) == 0
    return is_valid, cleaned if is_valid else {}, errors
