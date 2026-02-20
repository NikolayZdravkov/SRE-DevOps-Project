import pytest
from app import create_app, db
from sqlalchemy.pool import StaticPool

@pytest.fixture
def client():
    app = create_app({                                                                                      
        'TESTING': True,                                                                                    
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'connect_args': {'check_same_thread': False},
            'poolclass': StaticPool
        }
    })

    with app.app_context():
        db.create_all()

    yield app.test_client()

    with app.app_context():
        db.drop_all()


def test_healthcheck(client):
    response = client.get('/api/v1/healthcheck')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}  

def test_create_student(client):
    response = client.post('/api/v1/students', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "age": 22
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['first_name'] == 'John'
    assert data['last_name'] == 'Doe'
    assert data['email'] == 'john@example.com'
    assert data['age'] == 22

def test_get_students(client):
    client.post('/api/v1/students', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "age": 22
    })
    response = client.get('/api/v1/students')
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_get_student(client):
    client.post('/api/v1/students', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "age": 22
    })
    response = client.get('/api/v1/students/1')
    assert response.status_code == 200
    assert response.get_json()['email'] == 'john@example.com'

def test_get_student_not_found(client):
    response = client.get('/api/v1/students/999')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Student not found"}

def test_update_student(client):
    client.post('/api/v1/students', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "age": 22
    })
    response = client.put('/api/v1/students/1', json={"age": 25})
    assert response.status_code == 200
    assert response.get_json()['age'] == 25

def test_delete_student(client):
    client.post('/api/v1/students', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "age": 22
    })
    response = client.delete('/api/v1/students/1')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Student deleted successfully"}

    response = client.get('/api/v1/students/1')
    assert response.status_code == 404

