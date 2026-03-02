from datetime import date, datetime, timedelta

from flask import request
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from sqlalchemy import distinct 
api = Api()
from backend.models import User,db,Patient,Doctor,Department,Appointment,Treatment

# Api routes for Login and Signup
from flask_jwt_extended import create_access_token

class Login(Resource):
    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and Password required"}, 400

        user = User.query.filter_by(email=email).first()

        if not user or user.password != password:
            return {"message": "Invalid Credentials"}, 401

        
        access_token = create_access_token(identity=user.email)

        # Redirect logic
        if user.role == 1:
            dashboard = "/admin/dashboard"
        elif user.role == 2:
            dashboard = "/doctor/dashboard"
        else:
            dashboard = "/patient/dashboard"

        return {
            "message": "Login Successful",
            "role": user.role,
            "redirect_to": dashboard,
            "access_token": access_token
        }, 200
    
class Signup(Resource):
    def post(self):
        data=request.get_json()

        first_name=data.get("first_name")
        last_name=data.get("last_name")
        email=data.get("email")
        age=data.get("age")
        gender=data.get("gender")
        address=data.get("address")
        phone=data.get("phone")
        dob=data.get("dob")
        insurance=data.get("insurance")
        password=data.get("password")

        if not email or not password:
            return {"message":"Email and Password are required"},400
        exist=User.query.filter_by(email=email).first()
        if exist:
            return{"message":"User already exists"},400
        new_user=User(email=email,password=password,role=3)
        db.session.add(new_user)
        db.session.commit()

        
        new_patient = Patient(first_name=first_name,last_name=last_name,email=email,age=age,gender=gender,address=address,phone=phone,dob=dob,insurance=insurance)
        db.session.add(new_patient)
        db.session.commit()
        return {"message": "Signup successful"}, 201
api.add_resource(Login, "/login")
api.add_resource(Signup, "/signup")
#Patient,Doctor and Admin Dashboard route 
class AdminDashboard(Resource):

    @jwt_required()
    def get(self):

        current_user = User.query.filter_by(
            email=get_jwt_identity()
        ).first()

        if not current_user or current_user.role != 1:
            return {"message": "Admin access only"}, 403

        doctors = Doctor.query.all()
        patients = Patient.query.all()
        appointments = Appointment.query.all()

        today = date.today()

        available_appointments = []
        past_appointments = []

        for a in appointments:

            doctor_obj = Doctor.query.get(a.Doc_id)
            patient_obj = Patient.query.get(a.Pat_id)

            app_data = {
                "App_id": a.id,
                "Date": str(a.Date),
                "Time": str(a.Time),
                "Status": a.Status,
                "doctor_name": f"{doctor_obj.First_Name} {doctor_obj.Last_Name}" if doctor_obj else None,
                "patient_name": f"{patient_obj.First_Name} {patient_obj.Last_Name}" if patient_obj else None
            }

            if a.Date < today:
                past_appointments.append(app_data)
            else:
                available_appointments.append(app_data)

        return {
            "doctor_count": len(doctors),
            "patient_count": len(patients),
            "appointment_count": len(appointments),
            "available_appointments": available_appointments,
            "past_appointments": past_appointments
        }, 200
