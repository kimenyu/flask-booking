from flask import request, jsonify
from app import db, app
from app.models import Nurse, Patient
from flask_jwt_extended import create_access_token
from flask_bcrypt import generate_password_hash, check_password_hash

def registerNurse():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    existing_user = Nurse.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    hashed_password = generate_password_hash(password).decode('utf-8')
    new_nurse = Nurse(username=username, password_hash=hashed_password)
    db.session.add(new_nurse)
    db.session.commit()
    return jsonify({'message': 'Nurse registered successfully'}), 201

def loginNurse():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    nurse = Nurse.query.filter_by(username=username).first()
    if not nurse or not check_password_hash(nurse.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=nurse.id)
    return jsonify({'access_token': access_token}), 200


def registerPatient():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    existing_user = Patient.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    hashed_password = generate_password_hash(password).decode('utf-8')
    new_patient = Patient(username=username, password_hash=hashed_password)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient registered successfully'}), 201

def loginPatient():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    patient = Patient.query.filter_by(username=username).first()
    if not patient or not check_password_hash(patient.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=patient.id)
    return jsonify({'access_token': access_token}), 200