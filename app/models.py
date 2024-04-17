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
    
class PatientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nurse_id = db.Column(db.Integer, db.ForeignKey('nurse.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
