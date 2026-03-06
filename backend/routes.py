from datetime import date, datetime, time, timedelta
from flask import request
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import distinct
from models import User, db, Patient, Doctor, Department, Appointment, Treatment,SLOT_LABELS ,SLOT_TIME_OBJECTS

api = Api()

#login and signup routes
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email", "").strip()
        password = str(data.get("password", "")).strip()

        if not email or not password:
            return {"message": "Email and password required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User not found", "redirect": "signup"}, 404

        if user.password != password:
            return {"message": "Incorrect password"}, 401

        # Create JWT token
        access_token = create_access_token(identity=user.email)

        # Role-based dashboard mapping
        if user.role == 1:        # Admin
            dashboard = "/admin/dashboard"
        elif user.role == 2:      # Doctor
            dashboard = "/doctor/dashboard"
        elif user.role == 3:      # Patient
            dashboard = "/patient/dashboard"
        else:
            dashboard = "/login"   # fallback

        return {
            "message": "Login Successful",
            "role": user.role,
            "redirect_to": dashboard,
            "access_token": access_token
        }, 200

class Signup(Resource):
    def post(self):
        data = request.get_json()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and Password are required"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 400

        new_user = User(email=email, password=password, role=3)
        db.session.add(new_user)
        db.session.commit()

        new_patient = Patient(
            first_name=first_name,
            last_name=last_name,
            email=email,
            age=data.get("age"),
            gender=data.get("gender"),
            address=data.get("address"),
            phone=data.get("phone"),
            dob=data.get("dob"),
            insurance=data.get("insurance")
        )
        db.session.add(new_patient)
        db.session.commit()

        return {"message": "Signup successful"}, 201


api.add_resource(Login, "/login")
api.add_resource(Signup, "/signup")

#Admin, Doctor and Patient Dashboard routes
class AdminDashboard(Resource):
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        doctors = Doctor.query.all()
        patients = Patient.query.all()
        appointments = Appointment.query.all()
        today = date.today()

        # convert to simple dicts with blacklist Status
        doctor_list = [
            {"id": d.id, "first_name": d.first_name, "last_name": d.last_name,
             "is_blacklisted": True if getattr(d, 'blacklisted', None) == "Y" else False}
            for d in doctors
        ]
        patient_list = [
            {"id": p.id, "first_name": p.first_name, "last_name": p.last_name,
             "is_blacklisted": True if getattr(p, 'blacklisted', None) == "Y" else False}
            for p in patients
        ]

        available_appointments = []
        past_appointments = []

        for a in appointments:
            doctor_obj = Doctor.query.get(a.doctor_id)
            patient_obj = Patient.query.get(a.patient_id)

            app_data = {
                "id": a.id,
                "date": str(a.date),
                "time": str(a.time),
                "Status": a.Status,
                "doctor_name": f"{doctor_obj.first_name} {doctor_obj.last_name}" if doctor_obj else None,
                "patient_name": f"{patient_obj.first_name} {patient_obj.last_name}" if patient_obj else None
            }

            if a.date < today:
                past_appointments.append(app_data)
            else:
                available_appointments.append(app_data)

        return {
            "doctors": doctor_list,
            "patients": patient_list,
            "doctor_count": len(doctor_list),
            "patient_count": len(patient_list),
            "appointment_count": len(appointments),
            "available_appointments": available_appointments,
            "past_appointments": past_appointments
        }, 200


class PatientDashboard(Resource):
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()
        patient_record = Patient.query.filter_by(email=current_user.email).first()

        if not patient_record:
            return {"message": "Patient record not found"}, 404

        pat_id = patient_record.id
        today = datetime.now().date()
        next_week = today + timedelta(days=7)

        upcoming_appointments = (
            Appointment.query
            .filter(Appointment.patient_id == pat_id, Appointment.date >= today, Appointment.date <= next_week)
            .order_by(Appointment.date, Appointment.time)
            .all()
        )

        future_appointments = [
            {
                "App_id": a.id,
                "Date": str(a.date),
                "Time": str(a.time),
                "Status": a.Status
            }
            for a in upcoming_appointments
            if datetime.combine(a.date, a.time) >= datetime.now()
        ]

        treatment_records = (
            db.session.query(Treatment, Appointment, Doctor)
            .join(Appointment, Treatment.appointment_id == Appointment.id)
            .join(Doctor, Appointment.doctor_id == Doctor.id)
            .filter(Appointment.patient_id == pat_id)
            .order_by(Appointment.date.desc())
            .all()
        )

        treatment_history = [
            {
                "Treatment_id": t.id,
                "Prescription": t.prescription,
                "Date": str(a.date),
                "Doctor": f"{d.first_name} {d.last_name}"
            }
            for t, a, d in treatment_records
        ]

        doctors_list = [{"Doc_id": d.id, "Name": f"{d.first_name} {d.last_name}", "Department": d.department_id} for d in Doctor.query.all()]
        departments_list = [{"Dept_id": dep.id, "Dept_name": dep.name} for dep in Department.query.all()]

        return {
            "patient": {"patient_id": patient_record.id, "name": f"{patient_record.first_name} {patient_record.last_name}", "email": patient_record.email},
            "upcoming_appointments": future_appointments,
            "treatment_history": treatment_history,
            "doctors": doctors_list,
            "departments": departments_list
        }, 200

class DoctorDashboard(Resource):

    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()

            doctor = Doctor.query.filter_by(email=email).first()
            if not doctor:
                return {"message": "Doctor not found"}, 404

            doc_id = doctor.id
            today = date.today()
            tomorrow = today + timedelta(days=1)
            next_week = today + timedelta(days=7)

            # Today's appointments
            todays_query = (
                db.session.query(Appointment, Patient)
                .join(Patient, Appointment.patient_id == Patient.id)
                .filter(
                    Appointment.doctor_id == doc_id,
                    Appointment.status.ilike("Booked"),   # <-- fixed lowercase
                    Appointment.date == today
                )
                .order_by(Appointment.time)
                .all()
            )

            todays = [{
                "id": a.id,
                "date": str(a.date),
                "time": str(a.time),
                "status": a.status,   # <-- lowercase
                "patient_name": f"{p.first_name} {p.last_name}"
            } for a, p in todays_query]

            # Upcoming appointments (next 7 days)
            upcoming_query = (
                db.session.query(Appointment, Patient)
                .join(Patient, Appointment.patient_id == Patient.id)
                .filter(
                    Appointment.doctor_id == doc_id,
                    Appointment.status.ilike("Booked"),   # <-- lowercase
                    Appointment.date >= tomorrow,
                    Appointment.date <= next_week
                )
                .order_by(Appointment.date, Appointment.time)
                .all()
            )

            upcoming = [{
                "id": a.id,
                "date": str(a.date),
                "time": str(a.time),
                "status": a.status,   # <-- lowercase
                "patient_name": f"{p.first_name} {p.last_name}"
            } for a, p in upcoming_query]

            # Past appointments
            past_query = (
                db.session.query(Appointment, Patient)
                .join(Patient, Appointment.patient_id == Patient.id)
                .filter(
                    Appointment.doctor_id == doc_id,
                    Appointment.date < today
                )
                .order_by(Appointment.date.desc())
                .all()
            )

            past = [{
                "id": a.id,
                "date": str(a.date),
                "time": str(a.time),
                "status": a.status,  # <-- lowercase
                "patient_name": f"{p.first_name} {p.last_name}"
            } for a, p in past_query]

            # Assigned patients (distinct)
            assigned_query = (
                db.session.query(Patient)
                .join(Appointment, Appointment.patient_id == Patient.id)
                .filter(Appointment.doctor_id == doc_id)
                .distinct()
                .all()
            )

            patients = [{
                "id": p.id,
                "first_name": p.first_name,
                "last_name": p.last_name,
                "email": p.email
            } for p in assigned_query]

            return {
                "todays": todays,
                "upcoming": upcoming,
                "past": past,
                "patients": patients
            }, 200

        except Exception as e:
            print("DoctorDashboard error:", e)
            return {"message": "Internal Server Error"}, 500

api.add_resource(DoctorDashboard, "/doctor/dashboard")
api.add_resource(AdminDashboard, "/admin/dashboard")
api.add_resource(PatientDashboard, "/patient/dashboard")

#admin route to add doctor and department, only admin can access this route
class AddDoctor(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can add doctor"}, 403

        data = request.get_json()
        dept_name = data.get("deptname")
        dept_desc = data.get("deptdes")

        if not dept_name:
            return {"message": "Department name required"}, 400

        dept = Department.query.filter_by(name=dept_name).first()
        if not dept:
            dept = Department(name=dept_name, description=dept_desc)
            db.session.add(dept)
            db.session.commit()

        # create associated user account for doctor (role=2)
        doctor_email = data.get("email")
        if User.query.filter_by(email=doctor_email).first():
            return {"message": "User with this email already exists"}, 400

        new_user = User(email=doctor_email, password=data.get("password"), role=2)
        db.session.add(new_user)
        db.session.commit()

        new_doctor = Doctor(
            first_name=data.get("fn"),
            last_name=data.get("ln"),
            email=data.get("email"),
            age=data.get("age"),
            contact=data.get("contact"),
            experience=data.get("exp"),
            department_id=dept.id
        )
        db.session.add(new_doctor)
        db.session.commit()
        return {"message": "Doctor added successfully"}, 201

api.add_resource(AddDoctor, "/add_doctor")
#admin route to update doctor, only admin can access this route
class UpdateDoctor(Resource):
    @jwt_required()
    def put(self, doctor_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can update doctor"}, 403

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {"message": "Doctor not found"}, 404

        data = request.get_json()
        doctor.first_name = data.get("fn", doctor.first_name)
        doctor.last_name = data.get("ln", doctor.last_name)
        doctor.age = data.get("age", doctor.age)
        doctor.contact = data.get("contact", doctor.contact)
        doctor.experience = data.get("exp", doctor.experience)

        dept_name = data.get("deptname")
        if dept_name:
            dept_desc = data.get("deptdes")
            dept = Department.query.filter_by(name=dept_name).first()
            if not dept:
                dept = Department(name=dept_name, description=dept_desc)
                db.session.add(dept)
                db.session.commit()
            doctor.department_id = dept.id

        db.session.commit()
        return {"message": "Doctor updated successfully"}, 200
api.add_resource(UpdateDoctor, "/update_doctor/<int:doctor_id>")

#Api route to get doctor details by ID, only admin can access this route
class GetDoctor(Resource):
    @jwt_required()
    def get(self, doctor_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can view doctor details"}, 403

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {"message": "Doctor not found"}, 404

        return {
            "id": doctor.id,
            "first_name": doctor.first_name,
            "last_name": doctor.last_name,
            "email": doctor.email,
            "age": doctor.age,
            "contact": doctor.contact,
            "experience": doctor.experience,
            "department_id": doctor.department_id,
            "is_blacklisted": True if doctor.blacklisted == "Y" else False
        }, 200

api.add_resource(GetDoctor, "/get_doctor/<int:doctor_id>")
#Api route to delete doctor, only admin can access this route
class DeleteDoctor(Resource):
    @jwt_required()
    def delete(self, doctor_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can delete doctor"}, 403

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {"message": "Doctor not found"}, 404

        # delete associated user account
        user = User.query.filter_by(email=doctor.email).first()
        if user:
            db.session.delete(user) 
        db.session.delete(doctor)
        db.session.commit()
        return {"message": "Doctor deleted successfully"}, 200
api.add_resource(DeleteDoctor, "/delete_doctor/<int:doctor_id>")
#admin route to blacklist doctor, only admin can access this route
class BlacklistDoctor(Resource):
    @jwt_required()
    def post(self, doctor_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can blacklist doctor"}, 403

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {"message": "Doctor not found"}, 404

        # set flag to 'Y'
        doctor.blacklisted = "Y"
        db.session.commit()
        return {"message": "Doctor blacklisted successfully"}, 200
api.add_resource(BlacklistDoctor, "/blacklist_doctor/<int:doctor_id>")
#admin route to remove doctor from blacklist, only admin can access this route
class RemoveBlacklistDoctor(Resource):
    @jwt_required()
    def post(self, doctor_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can remove doctor from blacklist"}, 403

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {"message": "Doctor not found"}, 404

        # reset flag to 'N'
        doctor.blacklisted = "N"
        db.session.commit()
        return {"message": "Doctor removed from blacklist successfully"}, 200
api.add_resource(RemoveBlacklistDoctor, "/remove_blacklist_doctor/<int:doctor_id>")
#admin route to update patient, only admin can access this route
class UpdatePatient(Resource):
    @jwt_required()
    def put(self, patient_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can update patient"}, 403

        patient = Patient.query.get(patient_id)
        if not patient:
            return {"message": "Patient not found"}, 404

        data = request.get_json()
        patient.first_name = data.get("fn", patient.first_name)
        patient.last_name = data.get("ln", patient.last_name)
        patient.age = data.get("age", patient.age)
        patient.phone = data.get("phone", patient.phone)
        patient.gender = data.get("gender", patient.gender)
        patient.address = data.get("address", patient.address)
        patient.dob = data.get("dob", patient.dob)
        patient.insurance = data.get("insurance", patient.insurance)
        db.session.commit()
        return {"message": "Patient updated successfully"}, 200
api.add_resource(UpdatePatient, "/update_patient/<int:patient_id>")

#Api route to get patient details by ID, only admin can access this route
class GetPatient(Resource):
    @jwt_required()
    def get(self, patient_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can view patient details"}, 403

        patient = Patient.query.get(patient_id)
        if not patient:
            return {"message": "Patient not found"}, 404

        return {
            "id": patient.id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email,
            "age": patient.age,
            "gender": patient.gender,
            "address": patient.address,
            "phone": patient.phone,
            "dob": str(patient.dob) if patient.dob else None,
            "insurance": patient.insurance,
            "is_blacklisted": True if patient.blacklisted == "Y" else False
        }, 200

api.add_resource(GetPatient, "/get_patient/<int:patient_id>")
#admin route to delete patient, only admin can access this route
class DeletePatient(Resource):
    @jwt_required()
    def delete(self, patient_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can delete patient"}, 403

        patient = Patient.query.get(patient_id)
        if not patient:
            return {"message": "Patient not found"}, 404

        # delete associated user account
        user = User.query.filter_by(email=patient.email).first()
        if user:
            db.session.delete(user) 
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted successfully"}, 200
api.add_resource(DeletePatient, "/delete_patient/<int:patient_id>")
#admin route to blacklist patient, only admin can access this route
class BlacklistPatient(Resource):
    @jwt_required()
    def post(self, patient_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can blacklist patient"}, 403

        patient = Patient.query.get(patient_id)
        if not patient:
            return {"message": "Patient not found"}, 404

        # set flag to 'Y'
        patient.blacklisted = "Y"
        db.session.commit()
        return {"message": "Patient blacklisted successfully"}, 200
api.add_resource(BlacklistPatient, "/blacklist_patient/<int:patient_id>")
#admin route to remove patient from blacklist, only admin can access this route
class RemoveBlacklistPatient(Resource):
    @jwt_required()
    def post(self, patient_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can remove patient from blacklist"}, 403

        patient = Patient.query.get(patient_id)
        if not patient:
            return {"message": "Patient not found"}, 404

        # reset flag to 'N'
        patient.blacklisted = "N"
        db.session.commit()
        return {"message": "Patient removed from blacklist successfully"}, 200
api.add_resource(RemoveBlacklistPatient, "/remove_blacklist_patient/<int:patient_id>")
#api for searching doctors by name or department and search patient by name or email, only admin can access this route
class Search(Resource):
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Only admin can perform search"}, 403

        query = request.args.get("query", "").strip()
        if not query:
            return {"message": "Search query required"}, 400

        doctor_results = Doctor.query.join(Department).filter(
            (Doctor.first_name.ilike(f"%{query}%")) |
            (Doctor.last_name.ilike(f"%{query}%")) |
            (Department.name.ilike(f"%{query}%"))
        ).all()

        patient_results = Patient.query.filter(
            (Patient.first_name.ilike(f"%{query}%")) |
            (Patient.last_name.ilike(f"%{query}%")) |
            (Patient.email.ilike(f"%{query}%"))
        ).all()

        doctors = [{"id": d.id, "first_name": d.first_name, "last_name": d.last_name, "department": d.department.name if d.department else None} for d in doctor_results]
        patients = [{"id": p.id, "first_name": p.first_name, "last_name": p.last_name, "email": p.email} for p in patient_results]

        return {"doctors": doctors, "patients": patients}, 200
api.add_resource(Search, "/search")
class editPatient(Resource):
    @jwt_required()
    def put(self, patient_id):
        user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=user_email).first()

        if current_user.role != 1:
            return {"message": "Only admin can update patient"}, 403

        patient = Patient.query.get(patient_id)
        if not patient:
            return {"message": "Patient not found"}, 404

        data = request.get_json()
        patient.first_name = data.get("fn", patient.first_name)
        patient.last_name = data.get("ln", patient.last_name)
        patient.age = data.get("age", patient.age)
        patient.phone = data.get("phone", patient.phone)

class ManageSlots(Resource):
    @jwt_required()
    def get(self):
        """Return next 7 days slots for the doctor with status."""
        email = get_jwt_identity()
        doctor = Doctor.query.filter_by(email=email).first()
        if not doctor:
            return {"message": "Doctor not found"}, 404

        today = date.today()
        now = datetime.now().time()
        dates = [(today + timedelta(days=i)).isoformat() for i in range(7)]
        slots = {}

        for d in dates:
            day_date = datetime.strptime(d, "%Y-%m-%d").date()
            day_slots = []

            for key, slot_time in SLOT_TIME_OBJECTS.items():
                # Skip past slots for today
                if day_date == today and slot_time < now:
                    continue

                appt = Appointment.query.filter_by(
                    doctor_id=doctor.id,
                    date=day_date,
                    time=slot_time
                ).first()

                if appt:
                    if appt.patient_id:
                        status = "Booked"
                    else:
                        status = "Available"
                else:
                    status = "Not Created"

                day_slots.append({
                    "time_key": key,
                    "label": SLOT_LABELS.get(key, key),
                    "status": status,
                    "is_booked": status == "Booked",
                    "is_available": status == "Available"
                })

            slots[d] = day_slots

        return {"dates": dates, "slots": slots}, 200

    @jwt_required()
    def post(self):
        """Doctor adds new slots for upcoming days."""
        data = request.get_json()
        slot_list = data.get("slots", [])
        email = get_jwt_identity()
        doctor = Doctor.query.filter_by(email=email).first()
        if not doctor:
            return {"message": "Doctor not found"}, 404

        added = 0
        for slot in slot_list:
            day, time_key = slot.split("|")
            day_date = datetime.strptime(day, "%Y-%m-%d").date()
            time_obj = SLOT_TIME_OBJECTS.get(time_key)
            if not time_obj:
                continue

            existing = Appointment.query.filter_by(
                doctor_id=doctor.id,
                date=day_date,
                time=time_obj
            ).first()

            if not existing:
                new_slot = Appointment(
                    doctor_id=doctor.id,
                    date=day_date,
                    time=time_obj,
                    patient_id=None
                )
                db.session.add(new_slot)
                added += 1

        db.session.commit()
        return {"message": f"{added} slots added successfully"}, 201


class CancelSlotAPI(Resource):
    @jwt_required()
    def post(self):
        """Cancel a slot: free if booked, delete if available."""
        data = request.get_json()
        day = data.get("day")
        time_key = data.get("time")
        email = get_jwt_identity()
        doctor = Doctor.query.filter_by(email=email).first()
        if not doctor:
            return {"message": "Doctor not found"}, 404

        day_date = datetime.strptime(day, "%Y-%m-%d").date()
        time_obj = SLOT_TIME_OBJECTS.get(time_key)
        if not time_obj:
            return {"message": "Invalid time slot"}, 400

        appt = Appointment.query.filter_by(
            doctor_id=doctor.id,
            date=day_date,
            time=time_obj
        ).first()

        if not appt:
            return {"message": "Slot not found"}, 404

        if appt.patient_id:
            appt.patient_id = None
        else:
            db.session.delete(appt)

        db.session.commit()
        return {"message": "Slot cancelled successfully"}, 200


class ViewSlots(Resource):
    @jwt_required()
    def get(self):
        """Return slots for next 7 days including status for frontend rendering."""
        email = get_jwt_identity()
        doctor = Doctor.query.filter_by(email=email).first()
        if not doctor:
            return {"message": "Doctor not found"}, 404

        today = date.today()
        slots = []

        for day_offset in range(7):
            day_date = today + timedelta(days=day_offset)
            for key, time_obj in SLOT_TIME_OBJECTS.items():
                appt = Appointment.query.filter_by(
                    doctor_id=doctor.id,
                    date=day_date,
                    time=time_obj
                ).first()

                if appt:
                    if appt.patient_id:
                        status = "Booked"
                    else:
                        status = "Available"
                else:
                    status = "Not Created"

                slots.append({
                    "date": day_date.strftime("%Y-%m-%d"),
                    "time_key": key,
                    "label": SLOT_LABELS.get(key, key),
                    "status": status,
                    "is_booked": status == "Booked",
                    "is_available": status == "Available"
                })

        return {"slots": slots}, 200

api.add_resource(ManageSlots, "/manage_slots")
api.add_resource(CancelSlotAPI, "/cancel_slot")
api.add_resource(ViewSlots, "/view_slots")