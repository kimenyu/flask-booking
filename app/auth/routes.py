from flask import Blueprint
from . import controllers

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register-nurse', methods=['POST'])(controllers.registerNurse)
auth_bp.route('/register-patient', methods=['POST'])(controllers.registerPatient)
auth_bp.route('/login-nurse', methods=['POST'])(controllers.loginNurse)
auth_bp.route('/login-patient', methods=['POST'])(controllers.loginPatient)
