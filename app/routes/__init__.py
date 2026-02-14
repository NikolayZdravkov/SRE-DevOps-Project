from flask import Blueprint, jsonify, request
from app import db
from app.models import Student

api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"}), 200

@api.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()

    if not data or not all(key in data for key in ['first_name', 'email']):
        return jsonify({"error": "first_name, last_name, and email required"}), 400
        
    student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        age=data.get('age')
    )

    db.session.add(student)
    db.session.commit()

    return jsonify(student.to_dict()), 201

@api.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students]), 200

@api.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student.to_dict()), 200

@api.route('/students/<int:id>', methods=['PUT'])                                                        
def update_student(id):
    student = Student.query.get(id)                                                                      
    if not student:                                                                                      
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()

    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.email = data.get('email', student.email)
    student.age = data.get('age', student.age)

    db.session.commit()

    return jsonify(student.to_dict()), 200


@api.route('/students/<int:id>', methods=['DELETE'])                                                     
def delete_student(id):
    student = Student.query.get(id)                                                                      
    if not student:                                                                                      
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"}), 200