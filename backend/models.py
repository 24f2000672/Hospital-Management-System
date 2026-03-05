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
# ---------------- MODELS ----------------

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
