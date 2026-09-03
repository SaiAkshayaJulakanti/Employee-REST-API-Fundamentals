"""
Comprehensive Integration Test Suite for Employee REST API.
"""
import json

def test_health_check(client):
    """Test GET /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_root_endpoint(client):
    """Test GET / endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Employee REST API'


def test_create_employee_success(client):
    """Test POST /employees creates employee and returns 201 Created."""
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "department": "Engineering",
        "role": "Senior Software Engineer",
        "salary": 95000.0
    }
    response = client.post('/employees', json=payload)
    assert response.status_code == 201
    assert 'Location' in response.headers
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['name'] == "Jane Doe"
    assert data['data']['email'] == "jane.doe@example.com"
    assert data['data']['salary'] == 95000.0
    assert 'id' in data['data']


def test_create_employee_missing_fields(client):
    """Test POST /employees with missing required fields returns 400 Bad Request."""
    payload = {
        "name": "Incomplete User",
        "email": "incomplete@example.com"
        # missing department, role, salary
    }
    response = client.post('/employees', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['code'] == 400
    assert 'department' in data['errors']
    assert 'role' in data['errors']
    assert 'salary' in data['errors']


def test_create_employee_invalid_email(client):
    """Test POST /employees with invalid email format returns 400 Bad Request."""
    payload = {
        "name": "Bad Email",
        "email": "not-an-email",
        "department": "Sales",
        "role": "Sales Rep",
        "salary": 50000.0
    }
    response = client.post('/employees', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'email' in data['errors']


def test_create_employee_negative_salary(client):
    """Test POST /employees with negative salary returns 400 Bad Request."""
    payload = {
        "name": "Bob Builder",
        "email": "bob@example.com",
        "department": "Construction",
        "role": "Architect",
        "salary": -500.0
    }
    response = client.post('/employees', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'salary' in data['errors']


def test_create_employee_duplicate_email(client, sample_employee):
    """Test POST /employees with duplicate email returns 409 Conflict."""
    payload = {
        "name": "Duplicate Person",
        "email": sample_employee['email'], # Existing email
        "department": "Engineering",
        "role": "DevOps Engineer",
        "salary": 80000.0
    }
    response = client.post('/employees', json=payload)
    assert response.status_code == 409
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['code'] == 409
    assert 'already exists' in data['message']


def test_create_employee_non_json(client):
    """Test POST /employees without application/json header returns error."""
    response = client.post('/employees', data="plain text data", content_type="text/plain")
    assert response.status_code in [400, 415]


def test_get_all_employees(client, sample_employee):
    """Test GET /employees returns list of employees."""
    response = client.get('/employees')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)
    assert len(data['data']) == 1
    assert data['pagination']['total'] == 1


def test_get_employees_filter_by_department(client, sample_employee):
    """Test GET /employees?department=Engineering returns filtered results."""
    # Filter matching department
    res1 = client.get('/employees?department=Engineering')
    assert res1.status_code == 200
    data1 = res1.get_json()
    assert len(data1['data']) == 1

    # Filter non-matching department
    res2 = client.get('/employees?department=Marketing')
    assert res2.status_code == 200
    data2 = res2.get_json()
    assert len(data2['data']) == 0


def test_get_employees_search(client, sample_employee):
    """Test GET /employees?search=Alice returns matching employees."""
    response = client.get('/employees?search=Alice')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['data']) == 1
    assert data['data'][0]['name'] == "Alice Smith"


def test_get_employee_by_id_success(client, sample_employee):
    """Test GET /employees/{id} returns specified employee."""
    emp_id = sample_employee['id']
    response = client.get(f'/employees/{emp_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['id'] == emp_id
    assert data['data']['email'] == sample_employee['email']


def test_get_employee_by_id_not_found(client):
    """Test GET /employees/9999 returns 404 Not Found."""
    response = client.get('/employees/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['code'] == 404


def test_update_employee_full_put_success(client, sample_employee):
    """Test PUT /employees/{id} updates all attributes of an employee."""
    emp_id = sample_employee['id']
    update_payload = {
        "name": "Alice Smith Updated",
        "email": "alice.updated@example.com",
        "department": "Product Engineering",
        "role": "Lead Architect",
        "salary": 110000.0
    }
    response = client.put(f'/employees/{emp_id}', json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['name'] == "Alice Smith Updated"
    assert data['data']['email'] == "alice.updated@example.com"
    assert data['data']['salary'] == 110000.0


def test_update_employee_full_put_invalid_id(client):
    """Test PUT /employees/9999 returns 404 Not Found."""
    update_payload = {
        "name": "Ghost Employee",
        "email": "ghost@example.com",
        "department": "HR",
        "role": "Manager",
        "salary": 60000.0
    }
    response = client.put('/employees/9999', json=update_payload)
    assert response.status_code == 404


def test_update_employee_partial_patch_success(client, sample_employee):
    """Test PATCH /employees/{id} updates specified attributes only."""
    emp_id = sample_employee['id']
    patch_payload = {
        "salary": 92000.0,
        "role": "Principal Developer"
    }
    response = client.patch(f'/employees/{emp_id}', json=patch_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['salary'] == 92000.0
    assert data['data']['role'] == "Principal Developer"
    # Name and email should remain unchanged
    assert data['data']['name'] == sample_employee['name']


def test_delete_employee_success(client, sample_employee):
    """Test DELETE /employees/{id} removes record and returns 200 OK."""
    emp_id = sample_employee['id']
    response = client.delete(f'/employees/{emp_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert f"ID {emp_id} deleted" in data['message']

    # Verify subsequent GET returns 404
    get_res = client.get(f'/employees/{emp_id}')
    assert get_res.status_code == 404


def test_delete_employee_not_found(client):
    """Test DELETE /employees/9999 returns 404 Not Found."""
    response = client.delete('/employees/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['code'] == 404


def test_method_not_allowed(client):
    """Test sending invalid HTTP method to endpoint returns 405 Method Not Allowed."""
    # PATCH is allowed on /employees/<id>, but not on /employees root collection
    response = client.patch('/employees', json={"salary": 1000})
    assert response.status_code == 405
    data = response.get_json()
    assert data['code'] == 405
