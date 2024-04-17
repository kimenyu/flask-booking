from flask import jsonify, request
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Nurse, Patient, Appointment, NurseProfile, Review, PatientProfile
from datetime import datetime


def protected_route():
    current_user_id = get_jwt_identity()
    nurse = Nurse.query.get(current_user_id)
    return jsonify({'message': f'Hello, {nurse.username}! This route is protected.'}), 200

#get all nurses
def get_all_nurses():
    nurses = Nurse.query.all()
    return jsonify([nurse.username for nurse in nurses]), 200

#get nurse by id
def get_nurse_by_id(nurse_id):
    nurse = Nurse.query.get_or_404(nurse_id)
    return jsonify(nurse.username), 200

#create appointment

@jwt_required()
def create_appointment():
    current_user_id = get_jwt_identity()
    patient = Patient.query.get(current_user_id)
    nurse_id = request.json.get('nurse_id')
    appointment_datetime = request.json.get('appointment_datetime')
    nurse = Nurse.query.get_or_404(nurse_id)

    if not nurse.is_Available:
        return jsonify({'message': 'Nurse is not available for appointments at this time'}), 400

    # Assuming appointment_datetime is in ISO format ("YYYY-MM-DDTHH:MM:SS")
    try:
        appointment_datetime = datetime.fromisoformat(appointment_datetime)
    except ValueError:
        return jsonify({'message': 'Invalid datetime format'}), 400

    appointment = Appointment(patient=patient, nurse=nurse, appointment_datetime=appointment_datetime)
    db.session.add(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment created successfully!'}), 201

#get all appointments plus it's details
def get_all_appointments():
    appointments = Appointment.query.all()
    return jsonify([{
        'appointment_id': appointment.id,
        'nurse': appointment.nurse.username,
        'patient': appointment.patient.username,
        'appointment_datetime': appointment.appointment_datetime
    } for appointment in appointments]), 200
    

#get patient appointments
@jwt_required()
def get_patient_appointments():
    current_user_id = get_jwt_identity()
    print("Current User ID:", current_user_id)  # Debugging line
    patient = Patient.query.get(current_user_id)
    print("Patient:", patient)  # Debugging line

    # Check if the authenticated user is a patient
    if not patient:
        return jsonify({'message': 'Unauthorized access. Only patients can access this endpoint.'}), 401

    appointments = patient.appointments

    return jsonify([{
        'appointment_id': appointment.id,
        'nurse': appointment.nurse.username,
        'appointment_datetime': appointment.appointment_datetime
    } for appointment in appointments]), 200


    

#get nurse appointments
@jwt_required()
def get_nurse_appointments():
    current_user_id = get_jwt_identity()
    print("Current User ID:", current_user_id)  # Debugging line

    nurse = Nurse.query.get(current_user_id)
    print("Patient:", nurse)  # Debugging line
    # Check if the authenticated user is a nurse
    if not nurse:
        return jsonify({'message': 'Unauthorized access. Only nurses can access this endpoint.'}), 401

    appointments = nurse.appointments

    return jsonify([{
        'appointment_id': appointment.id,
        'patient': appointment.patient.username,
        'appointment_datetime': appointment.appointment_datetime
    } for appointment in appointments]), 200


#update appointment
@jwt_required()
def update_appointment(appointment_id):
    current_user_id = get_jwt_identity()
    appointment = Appointment.query.filter_by(id=appointment_id).first_or_404()

    # Check if the appointment belongs to the authenticated user
    if appointment.patient_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    appointment_datetime = request.json.get('appointment_datetime')
    # Validate and update appointment_datetime
    try:
        updated_datetime = datetime.fromisoformat(appointment_datetime)
    except ValueError:
        return jsonify({'message': 'Invalid datetime format'}), 400

    appointment.appointment_datetime = updated_datetime
    db.session.commit()

    return jsonify({'message': 'Appointment updated successfully!'}), 200

#delete appointment
@jwt_required()
def delete_appointment(appointment_id):
    current_user_id = get_jwt_identity()
    appointment = Appointment.query.filter_by(id=appointment_id).first_or_404()

    # Check if the appointment belongs to the authenticated user
    if appointment.patient_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment deleted successfully!'}), 200


#create review - only patients can create reviews. Review for a nurse
@jwt_required()
def create_review():
    current_user_id = get_jwt_identity()
    patient = Patient.query.get(current_user_id)
    nurse_id = request.json.get('nurse_id')
    rating = request.json.get('rating')
    comment = request.json.get('comment')

    nurse = Nurse.query.get_or_404(nurse_id)
    review = Review(patient=patient, nurse=nurse, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review created successfully!'}), 201

#get reviews and average rating for a nurse
def get_nurse_reviews(nurse_id):
    nurse = Nurse.query.get_or_404(nurse_id)
    reviews = nurse.reviews
    average_rating = sum([review.rating for review in reviews]) / len(reviews) if reviews else 0

    return jsonify({
        'nurse': nurse.username,
        'average_rating': average_rating,
        'reviews': [{
            'patient': review.patient.username,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews]
    }), 200
    
#update review - only patients can update reviews
@jwt_required()
def update_review(review_id):
    current_user_id = get_jwt_identity()
    review = Review.query.filter_by(id=review_id).first_or_404()

    # Check if the review belongs to the authenticated user
    if review.patient_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    rating = request.json.get('rating')
    comment = request.json.get('comment')

    review.rating = rating
    review.comment = comment
    db.session.commit()

    return jsonify({'message': 'Review updated successfully!'}), 200

#delete review - only patients can delete their own reviews
@jwt_required()
def delete_review(review_id):
    current_user_id = get_jwt_identity()
    review = Review.query.filter_by(id=review_id).first_or_404()

    # Check if the review belongs to the authenticated user
    if review.patient_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted successfully!'}), 200

#get review by id
def get_review_by_id(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify({
        'patient': review.patient.username,
        'nurse': review.nurse.username,
        'rating': review.rating,
        'comment': review.comment
    }), 200
    
#create nurse profile - authenticated nurses can create their profiles. area of expertise should be a list
@jwt_required()
def create_nurse_profile():
    current_user_id = get_jwt_identity()
    nurse = Nurse.query.get(current_user_id)

    if not nurse:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    qualifications = data.get('qualifications')
    experience = data.get('experience')
    areas_of_expertise = data.get('areas_of_expertise')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')

    nurse_profile = NurseProfile(
        nurse_id=current_user_id,
        qualifications=qualifications,
        experience=experience,
        areas_of_expertise=areas_of_expertise,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=phone
    )

    try:
        db.session.add(nurse_profile)
        db.session.commit()
        return jsonify({'message': 'Nurse profile created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#update nurse profile - authenticated nurses can update their profiles
@jwt_required()
def update_nurse_profile():
    current_user_id = get_jwt_identity()

    # Check if the nurse profile exists
    nurse_profile = NurseProfile.query.filter_by(nurse_id=current_user_id).first()
    if not nurse_profile:
        return jsonify({'error': 'Nurse profile not found'}), 404

    # Update the nurse profile fields if provided in the request
    data = request.json
    if 'qualifications' in data:
        nurse_profile.qualifications = data['qualifications']
    if 'experience' in data:
        nurse_profile.experience = data['experience']
    if 'areas_of_expertise' in data:
        # Serialize the list into a string before assigning
        nurse_profile.areas_of_expertise = ','.join(data['areas_of_expertise'])
    if 'email' in data:
        nurse_profile.email = data['email']
    if 'first_name' in data:
        nurse_profile.first_name = data['first_name']
    if 'last_name' in data:
        nurse_profile.last_name = data['last_name']
    if 'phone' in data:
        nurse_profile.phone = data['phone']

    try:
        db.session.commit()
        return jsonify({'message': 'Nurse profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#get nurse profile - authenticated nurses can get their profiles
@jwt_required()
def get_nurse_profile():
    current_user_id = get_jwt_identity()
    nurse = Nurse.query.get(current_user_id)
    nurse_profile = nurse.nurse_profile

    return jsonify({
        'qualifications': nurse_profile.qualifications,
        'experience': nurse_profile.experience,
        'areas_of_expertise': nurse_profile.areas_of_expertise,
        'email': nurse_profile.email,
        'first_name': nurse_profile.first_name,
        'last_name': nurse_profile.last_name,
        'phone': nurse_profile.phone
    }), 200
    
#create patient profile - authenticated patients can create their profiles
@jwt_required()
def create_patient_profile():
    current_user_id = get_jwt_identity()
    patient = Patient.query.get(current_user_id)

    email = request.json.get('email')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    phone = request.json.get('phone')

    patient_profile = PatientProfile(patient=patient, email=email, first_name=first_name, last_name=last_name, phone=phone)
    db.session.add(patient_profile)
    db.session.commit()

    return jsonify({'message': 'Patient profile created successfully!'}), 201

#update patient profile - authenticated patients can update their profiles
@jwt_required()
def update_patient_profile():
    current_user_id = get_jwt_identity()
    patient = Patient.query.get(current_user_id)
    patient_profile = patient.patient_profile

    email = request.json.get('email')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    phone = request.json.get('phone')

    patient_profile.email = email
    patient_profile.first_name = first_name
    patient_profile.last_name = last_name
    patient_profile.phone = phone

    db.session.commit()

    return jsonify({'message': 'Patient profile updated successfully!'}), 200

#get patient profile - authenticated patients can get their profiles
@jwt_required()
def get_patient_profile():
    current_user_id = get_jwt_identity()
    patient = Patient.query.get(current_user_id)
    patient_profile = patient.patient_profile

    return jsonify({
        'email': patient_profile.email,
        'first_name': patient_profile.first_name,
        'last_name': patient_profile.last_name,
        'phone': patient_profile.phone
    }), 200