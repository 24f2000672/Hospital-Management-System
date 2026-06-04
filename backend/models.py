from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from datetime import datetime, time

db = SQLAlchemy()

SLOT_TIME_OBJECTS = {
    "09:00": time(9, 0),
    "10:00": time(10, 0),
    "11:00": time(11, 0),
    "12:00": time(12, 0),
    "16:00": time(16, 0),
    "17:00": time(17, 0),
    "18:00": time(18, 0),
    "19:00": time(19, 0),
    "20:00": time(20, 0),
    "21:00": time(21, 0),
    "22:00": time(22, 0),
}
SLOT_LABELS = {
    "09:00": "09:00 AM",
    "10:00": "10:00 AM",
    "11:00": "11:00 AM",
    "12:00": "12:00 PM",
    "16:00": "04:00 PM",
    "17:00": "05:00 PM",
    "18:00": "06:00 PM",
    "19:00": "07:00 PM",
    "20:00": "08:00 PM",
    "21:00": "09:00 PM",
    "22:00": "10:00 PM",
}

# All the models required 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Integer)  # 1=Admin, 2=Doctor, 3=Patient


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    contact = db.Column(db.String(15))
    experience = db.Column(db.Integer)
    blacklisted = db.Column(db.String(2), default="N")

    department = db.relationship('Department', backref='doctors')
    appointments = db.relationship('Appointment', backref='doctor')


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    dob = db.Column(db.String, nullable=False)
    insurance = db.Column(db.String(2))
    blacklisted = db.Column(db.String(2), default="N")

    appointments = db.relationship('Appointment', backref='patient')


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(25), default="Available")


class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    diagnosis = db.Column(db.String(50))
    prescription = db.Column(db.String(50))
    notes = db.Column(db.String(100))
    progress = db.Column(db.String(25))

    appointment = db.relationship('Appointment', backref='treatments')


class ExportJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(128), unique=True, nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    status = db.Column(db.String(20), default="PENDING")
    file_path = db.Column(db.String(255), nullable=True)
    error_message = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    patient = db.relationship('Patient', backref='export_jobs')


class NotificationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(100), nullable=False)
    channel = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(120), nullable=True)
    message = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Health Guardian+ extensions

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), unique=True, nullable=False)
    blood_group = db.Column(db.String(10))
    allergies = db.Column(db.String(255))
    chronic_diseases = db.Column(db.String(255))
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    bmi = db.Column(db.Float)
    emergency_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('medical_record', uselist=False))


class HealthReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='health_reports')


class VitalSigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    heart_rate = db.Column(db.Integer)
    blood_pressure = db.Column(db.String(20))
    oxygen_level = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    sugar_level = db.Column(db.Float)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='vital_signs')


class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50))
    phone_number = db.Column(db.String(20), nullable=False)
    is_primary = db.Column(db.String(1), default='N')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='emergency_contacts')


class SOSLog(db.Model):
    __tablename__ = 'sos_log'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='sos_logs')


class EmergencyAlert(db.Model):
    __tablename__ = 'emergency_alert'
    id = db.Column(db.Integer, primary_key=True)
    sos_log_id = db.Column(db.Integer, db.ForeignKey('sos_log.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    response_status = db.Column(db.String(30), default='PENDING')
    contact_notified = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sos_log = db.relationship('SOSLog', backref=db.backref('alerts', lazy=True))


class MedicineReminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medicine_name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.String(80), nullable=False)
    reminder_time = db.Column(db.String(20), nullable=False)
    frequency = db.Column(db.String(40), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    active = db.Column(db.String(1), default='Y')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='medicine_reminders')


class MedicationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reminder_id = db.Column(db.Integer, db.ForeignKey('medicine_reminder.id'), nullable=False)
    taken_dose = db.Column(db.Integer, default=0)
    missed_dose = db.Column(db.Integer, default=0)
    compliance_percent = db.Column(db.Float, default=0.0)
    log_date = db.Column(db.Date, default=datetime.utcnow)

    reminder = db.relationship('MedicineReminder', backref='medication_history')


class SymptomCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    ai_prediction = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='symptom_checks')


class HealthRiskAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    disease_category = db.Column(db.String(100))
    recommendations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='risk_assessments')


class AccessibilitySettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), unique=True, nullable=False)
    voice_mode = db.Column(db.String(1), default='N')
    high_contrast = db.Column(db.String(1), default='N')
    large_text = db.Column(db.String(1), default='N')
    sign_language_mode = db.Column(db.String(1), default='N')
    vibration_alerts = db.Column(db.String(1), default='N')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('accessibility_settings', uselist=False))


class VideoConsultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    meeting_link = db.Column(db.String(255), nullable=False)
    scheduled_for = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), default='SCHEDULED')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship('Doctor', backref='video_consultations')
    patient = db.relationship('Patient', backref='video_consultations')


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('video_consultation.id'), nullable=False)
    sender_role = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    consultation = db.relationship('VideoConsultation', backref='messages')


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='AVAILABLE')
    notes = db.Column(db.String(255))


class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    admission_date = db.Column(db.DateTime, default=datetime.utcnow)
    discharge_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='ADMITTED')

    patient = db.relationship('Patient', backref='admissions')
    room = db.relationship('Room', backref='admissions')


class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=True)
    consultation_fees = db.Column(db.Float, default=0.0)
    medicine_fees = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='billings')
    admission = db.relationship('Admission', backref='billings')
class VaccinationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id'),
        nullable=False
    )

    vaccine_name = db.Column(db.String(100))
    dose_number = db.Column(db.Integer)
    vaccination_date = db.Column(db.Date)
    next_due_date = db.Column(db.Date)

    patient = db.relationship(
        'Patient',
        backref='vaccinations'
    )
class LabTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id')
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey('doctor.id')
    )

    test_name = db.Column(db.String(100))
    result = db.Column(db.Text)
    status = db.Column(db.String(30))
    test_date = db.Column(db.DateTime)

    patient = db.relationship(
        'Patient',
        backref='lab_tests'
    )

    doctor = db.relationship(
        'Doctor',
        backref='lab_tests'
    )
class AmbulanceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id')
    )

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    status = db.Column(
        db.String(30),
        default='REQUESTED'
    )

    requested_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    patient = db.relationship(
        'Patient',
        backref='ambulance_requests'
    )
class HealthGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id')
    )

    goal_name = db.Column(db.String(100))
    target_value = db.Column(db.Float)
    current_value = db.Column(db.Float)

    status = db.Column(
        db.String(20),
        default='ACTIVE'
    )

    patient = db.relationship(
        'Patient',
        backref='health_goals'
    )
class AIHealthAssistant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id')
    )

    question = db.Column(db.Text)
    response = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    patient = db.relationship(
        'Patient',
        backref='ai_queries'
    )