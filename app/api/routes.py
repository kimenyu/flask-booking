from flask import Blueprint
from . import controllers
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    current_user_id = get_jwt_identity()
    # Use current_user_id to retrieve user data from the database
    # Return response based on user type (Nurse or Patient)
    return jsonify({'message': 'Protected route accessed successfully'})


api_bp.route('/get_nurses', methods=['GET'])(controllers.get_all_nurses)
api_bp.route('/get_nurse/<int:nurse_id>', methods=['GET'])(controllers.get_nurse_by_id)

#appointments
api_bp.route('/create/appointment', methods=['POST'])(controllers.create_appointment)
api_bp.route('/get/appointments', methods=['GET'])(controllers.get_all_appointments)
api_bp.route('/get/patient/appointments', methods=['GET'])(controllers.get_patient_appointments)
api_bp.route('/get/nurse/appointments', methods=['GET'])(controllers.get_nurse_appointments)
api_bp.route('/update/appointment/<int:appointment_id>', methods=['PUT'])(controllers.update_appointment)
api_bp.route('/delete/appointment/<int:appointment_id>', methods=['DELETE'])(controllers.delete_appointment)

#reviews
api_bp.route('/create/review', methods=['POST'])(controllers.create_review)
api_bp.route('/get/nurse/reviews/<int:nurse_id>', methods=['GET'])(controllers.get_nurse_reviews)
api_bp.route('/update/review/<int:review_id>', methods=['PUT'])(controllers.update_review)
api_bp.route('/delete/review/<int:review_id>', methods=['DELETE'])(controllers.delete_review)
api_bp.route('/get/review/<int:review_id>', methods=['GET'])(controllers.get_review_by_id)


#nurse profile
api_bp.route('/create/nurse/profile', methods=['POST'])(controllers.create_nurse_profile)
api_bp.route('/get/nurse/profile', methods=['GET'])(controllers.get_nurse_profile)
api_bp.route('/update/nurse/profile', methods=['PUT'])(controllers.update_nurse_profile)

#patient profile
api_bp.route('/create/patient/profile', methods=['POST'])(controllers.create_patient_profile)
api_bp.route('/get/patient/profile', methods=['GET'])(controllers.get_patient_profile)
api_bp.route('/update/patient/profile', methods=['PUT'])(controllers.update_patient_profile)
