from app import db

class Nurse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    appointments = db.relationship('Appointment', backref='nurse', lazy=True)
    nurse_profile = db.relationship('NurseProfile', backref='nurse', uselist=False, lazy=True)
    reviews = db.relationship('Review', backref='nurse', lazy=True)
    is_Available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Nurse {self.username}>'

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    reviews = db.relationship('Review', backref='patient', lazy=True)

    def __repr__(self):
        return f'<Patient {self.username}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nurse_id = db.Column(db.Integer, db.ForeignKey('nurse.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    appointment_datetime = db.Column(db.DateTime, nullable=False)


class NurseProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nurse_id = db.Column(db.Integer, db.ForeignKey('nurse.id'), unique=True, nullable=False)
    qualifications = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.String(255), nullable=True)
    areas_of_expertise = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    def __init__(self, nurse_id, qualifications, experience, areas_of_expertise, email, first_name, last_name, phone):
        self.nurse_id = nurse_id
        self.qualifications = qualifications
        self.experience = experience
        self.areas_of_expertise = ', '.join(areas_of_expertise) if areas_of_expertise else None  # Convert list to string
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    def get_areas_of_expertise_list(self):
        return self.areas_of_expertise.split(', ') if self.areas_of_expertise else []

    
class PatientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    def __init__(self, patient=None, email=None, first_name=None, last_name=None, phone=None):
        self.patient = patient
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nurse_id = db.Column(db.Integer, db.ForeignKey('nurse.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
