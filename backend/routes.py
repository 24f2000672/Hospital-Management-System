from datetime import date, datetime, time, timedelta
from collections import Counter
import glob
import html
import os
from flask import request, send_file
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import distinct, or_
from models import User, db, Patient, Doctor, Department, Appointment, Treatment, ExportJob
from cache import cache_response, invalidate_cache

api = Api()

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


def _month_window_from_label(month_label):
    try:
        first_day = datetime.strptime(month_label, "%Y-%m").date()
    except ValueError:
        return None, None

    if first_day.month == 12:
        next_month = date(first_day.year + 1, 1, 1)
    else:
        next_month = date(first_day.year, first_day.month + 1, 1)
    return first_day, next_month


def _build_doctor_monthly_report(doctor_id, month_label):
    start_date, end_date = _month_window_from_label(month_label)
    if not start_date or not end_date:
        return None

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return None

    reports_root = os.path.join("instance", "reports", month_label)
    os.makedirs(reports_root, exist_ok=True)

    appointments = (
        db.session.query(Appointment, Patient)
        .outerjoin(Patient, Appointment.patient_id == Patient.id)
        .filter(
            Appointment.doctor_id == doctor.id,
            Appointment.date >= start_date,
            Appointment.date < end_date,
        )
        .order_by(Appointment.date, Appointment.time)
        .all()
    )

    treatments = (
        db.session.query(Treatment)
        .join(Appointment, Treatment.appointment_id == Appointment.id)
        .filter(
            Appointment.doctor_id == doctor.id,
            Appointment.date >= start_date,
            Appointment.date < end_date,
        )
        .all()
    )

    diagnosis_counts = Counter([t.diagnosis or "Unknown" for t in treatments])
    appointment_map = {a.id: (a, p) for a, p in appointments}
    report_path = os.path.join(reports_root, f"doctor_{doctor.id}_{month_label}.html")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("<html><head><title>Monthly Doctor Report</title></head><body>")
        f.write(f"<h1>Monthly Report - {month_label}</h1>")
        f.write(f"<h2>Doctor: {html.escape(doctor.first_name)} {html.escape(doctor.last_name)}</h2>")
        f.write(f"<p>Total appointments: {len(appointments)}</p>")
        f.write(f"<p>Total treatments: {len(treatments)}</p>")

        f.write("<h3>Diagnosis Summary</h3><ul>")
        if diagnosis_counts:
            for diagnosis, count in sorted(diagnosis_counts.items(), key=lambda x: x[0].lower()):
                f.write(f"<li>{html.escape(diagnosis)}: {count}</li>")
        else:
            f.write("<li>No diagnosis records in this month.</li>")
        f.write("</ul>")

        f.write("<h3>Appointments</h3><table border='1' cellpadding='6'>")
        f.write("<tr><th>ID</th><th>Date</th><th>Time</th><th>Status</th><th>Patient</th></tr>")
        for a, p in appointments:
            patient_name = f"{p.first_name} {p.last_name}" if p else "Unassigned"
            f.write(
                f"<tr><td>{a.id}</td><td>{a.date}</td><td>{a.time}</td><td>{html.escape(a.status or '')}</td><td>{html.escape(patient_name)}</td></tr>"
            )
        f.write("</table>")

        f.write("<h3>Treatments</h3><table border='1' cellpadding='6'>")
        f.write(
            "<tr><th>Treatment ID</th><th>Appointment ID</th><th>Date</th><th>Patient</th><th>Diagnosis</th><th>Prescription</th><th>Progress</th><th>Notes</th></tr>"
        )
        if treatments:
            for t in treatments:
                appt, patient = appointment_map.get(t.appointment_id, (None, None))
                appt_date = str(appt.date) if appt else "-"
                patient_name = f"{patient.first_name} {patient.last_name}" if patient else "Unassigned"

                f.write(
                    "<tr>"
                    f"<td>{t.id}</td>"
                    f"<td>{t.appointment_id}</td>"
                    f"<td>{appt_date}</td>"
                    f"<td>{html.escape(patient_name)}</td>"
                    f"<td>{html.escape(t.diagnosis or '')}</td>"
                    f"<td>{html.escape(t.prescription or '')}</td>"
                    f"<td>{html.escape(t.progress or '')}</td>"
                    f"<td>{html.escape(t.notes or '')}</td>"
                    "</tr>"
                )
        else:
            f.write("<tr><td colspan='8'>No treatments recorded in this month.</td></tr>")
        f.write("</table>")
        f.write("</body></html>")

    return {
        "report_path": report_path,
        "appointments": len(appointments),
        "treatments": len(treatments),
    }

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

        access_token = create_access_token(identity=user.email)

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

#Admin, Doctor and Patient Dashboard routes
class AdminDashboard(Resource):
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if current_user.role != 1:
            return {"message": "Access denied"}, 403

        doctors = Doctor.query.all()
        patients = Patient.query.all()
        appointments = Appointment.query.all()
        today = date.today()

        # convert to simple dicts with blacklist status
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
                "status": a.status,
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
            db.session.query(Appointment, Doctor)
            .join(Doctor, Appointment.doctor_id == Doctor.id)
            .filter(
                Appointment.patient_id == pat_id,
                Appointment.date >= today,
                Appointment.date <= next_week,
            )
            .order_by(Appointment.date, Appointment.time)
            .all()
        )

        future_appointments = [
            {
                "App_id": a.id,
                "Date": str(a.date),
                "Time": str(a.time),
                "Status": a.status,
                "Doctor": f"{d.first_name} {d.last_name}",
                "Doctor_id": d.id,
            }
            for a, d in upcoming_appointments
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


class PatientAvailableSlots(Resource):
    @jwt_required()
    @cache_response(ttl=600, prefix='available_slots', user_specific=True)
    def get(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or current_user.role != 3:
            return {"message": "Only patient can view available slots"}, 403

        today = date.today()
        next_week = today + timedelta(days=7)

        slots_query = (
            db.session.query(Appointment, Doctor)
            .join(Doctor, Appointment.doctor_id == Doctor.id)
            .filter(
                Appointment.status == "Available",
                Appointment.date >= today,
                Appointment.date <= next_week,
            )
            .order_by(Appointment.date, Appointment.time)
            .all()
        )

        slots = [
            {
                "App_id": a.id,
                "Date": str(a.date),
                "Time": str(a.time),
                "Doctor_id": d.id,
                "Doctor": f"{d.first_name} {d.last_name}",
            }
            for a, d in slots_query
        ]

        return {"available_slots": slots}, 200


class PatientBookSlot(Resource):
    @jwt_required()
    def post(self, slot_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or current_user.role != 3:
            return {"message": "Only patient can book slots"}, 403

        patient_record = Patient.query.filter_by(email=current_user.email).first()
        if not patient_record:
            return {"message": "Patient record not found"}, 404

        slot = Appointment.query.get(slot_id)
        if not slot:
            return {"message": "Slot not found"}, 404

        if slot.status != "Available":
            return {"message": "Slot is not available"}, 400

        slot.patient_id = patient_record.id
        slot.status = "Booked"
        db.session.commit()
        invalidate_cache("available_slots:*")
        
        return {"message": "Slot booked successfully"}, 200


class PatientCancelAppointment(Resource):
    @jwt_required()
    def post(self, booking_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or current_user.role != 3:
            return {"message": "Only patient can cancel appointments"}, 403

        patient_record = Patient.query.filter_by(email=current_user.email).first()
        if not patient_record:
            return {"message": "Patient record not found"}, 404

        booking = Appointment.query.get(booking_id)
        if not booking:
            return {"message": "Appointment not found"}, 404

        if booking.patient_id != patient_record.id:
            return {"message": "You can cancel only your appointments"}, 403

        if booking.status != "Booked":
            return {"message": "Only booked appointments can be cancelled"}, 400

        booking.patient_id = None
        booking.status = "Available"
        db.session.commit()
        invalidate_cache("available_slots:*")
        
        return {"message": "Appointment cancelled successfully"}, 200


class PatientExportTreatmentHistory(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or current_user.role != 3:
            return {"message": "Only patient can export treatment history"}, 403

        patient_record = Patient.query.filter_by(email=current_user.email).first()
        if not patient_record:
            return {"message": "Patient record not found"}, 404

        export_job = ExportJob(patient_id=patient_record.id, status="PENDING")
        db.session.add(export_job)
        db.session.commit()
        from tasks import export_treatment_history_csv

        task = export_treatment_history_csv.delay(export_job.id)
        export_job.task_id = task.id
        export_job.status = "QUEUED"
        db.session.commit()

        return {
            "message": "Export started",
            "job_id": export_job.id,
            "task_id": task.id,
            "status": export_job.status,
        }, 202


class PatientExportTreatmentHistoryStatus(Resource):
    @jwt_required()
    def get(self, job_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or current_user.role != 3:
            return {"message": "Only patient can view export status"}, 403

        patient_record = Patient.query.filter_by(email=current_user.email).first()
        if not patient_record:
            return {"message": "Patient record not found"}, 404

        export_job = ExportJob.query.get(job_id)
        if not export_job or export_job.patient_id != patient_record.id:
            return {"message": "Export job not found"}, 404

        # Check Celery task status if job is still in progress. This ensures we return updated status even if worker has completed the task but DB update is pending.
        if export_job.task_id and export_job.status in {"QUEUED", "RUNNING"}:
            from celery.result import AsyncResult
            from celery_app import celery

            task_state = AsyncResult(export_job.task_id, app=celery).state

            if task_state in {"FAILURE", "REVOKED"}:
                export_job.status = "FAILED"
                export_job.error_message = f"Task ended with state: {task_state}"
                export_job.completed_at = datetime.utcnow()
                db.session.commit()
            elif task_state == "PENDING" and export_job.created_at:
                age_seconds = (datetime.utcnow() - export_job.created_at).total_seconds()
                if age_seconds > 180:
                    export_job.status = "FAILED"
                    export_job.error_message = "Task is stale in queue. Please retry export."
                    export_job.completed_at = datetime.utcnow()
                    db.session.commit()

        return {
            "job_id": export_job.id,
            "task_id": export_job.task_id,
            "status": export_job.status,
            "error": export_job.error_message,
            "created_at": str(export_job.created_at) if export_job.created_at else None,
            "completed_at": str(export_job.completed_at) if export_job.completed_at else None,
            "download_url": f"/patient/export-treatment-history/{export_job.id}/download"
            if export_job.status == "COMPLETED" and export_job.file_path
            else None,
        }, 200


class PatientExportTreatmentHistoryDownload(Resource):
    @jwt_required()
    def get(self, job_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or current_user.role != 3:
            return {"message": "Only patient can download export"}, 403

        patient_record = Patient.query.filter_by(email=current_user.email).first()
        if not patient_record:
            return {"message": "Patient record not found"}, 404

        export_job = ExportJob.query.get(job_id)
        if not export_job or export_job.patient_id != patient_record.id:
            return {"message": "Export job not found"}, 404

        if export_job.status != "COMPLETED" or not export_job.file_path:
            return {"message": "Export file not ready"}, 400

        if not os.path.exists(export_job.file_path):
            return {"message": "Export file missing on server"}, 404

        return send_file(export_job.file_path, as_attachment=True)


class DoctorDashboard(Resource):
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()
        doctor_record = Doctor.query.filter_by(email=current_user.email).first()

        if not doctor_record:
            return {"message": "Doctor record not found"}, 404

        doc_id = doctor_record.id
        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)

        # all appointments for today with patient details
        todays_query = (
            db.session.query(Appointment, Patient)
            .join(Patient)
            .filter(Appointment.doctor_id == doc_id, Appointment.status == "Booked", Appointment.date == today)
            .order_by(Appointment.time)
            .all()
        )
        todays_appointments = [{"App_id": a.id, "Date": str(a.date), "Time": str(a.time), "Status": a.status, "Patient_Name": f"{p.first_name} {p.last_name}"} for a, p in todays_query]

        # all appointments for next 7 days with patient details
        upcoming_query = (
            db.session.query(Appointment, Patient)
            .join(Patient)
            .filter(Appointment.doctor_id == doc_id, Appointment.status == "Booked", Appointment.date >= tomorrow, Appointment.date <= next_week)
            .order_by(Appointment.date, Appointment.time)
            .all()
        )
        upcoming_appointments = [{"App_id": a.id, "Date": str(a.date), "Time": str(a.time), "Status": a.status, "Patient_Name": f"{p.first_name} {p.last_name}"} for a, p in upcoming_query]

        # previous/completed appointments with patient details
        past_query = (
            db.session.query(Appointment, Patient)
            .join(Patient)
            .filter(
                Appointment.doctor_id == doc_id,
                or_(Appointment.date < today, Appointment.status == "Completed"),
            )
            .order_by(Appointment.date.desc())
            .all()
        )
        past_appointments = [{"App_id": a.id, "Date": str(a.date), "Time": str(a.time), "Status": a.status, "Patient_Name": f"{p.first_name} {p.last_name}"} for a, p in past_query]

        # patients assigned to doctor 
        assigned_query = (
            db.session.query(Patient)
            .join(Appointment, Appointment.patient_id == Patient.id)
            .filter(Appointment.doctor_id == doc_id)
            .distinct()
            .all()
        )
        assigned_patients = [{"Pat_id": p.id, "Name": f"{p.first_name} {p.last_name}", "Email": p.email} for p in assigned_query]

        # dates in the next 7 days where no AVAILABLE slot exists. This helps doctor to identify dates where they need to add availability.
        availability_dates_query = (
            db.session.query(distinct(Appointment.date))
            .filter(
                Appointment.doctor_id == doc_id,
                Appointment.status == "Available",
                Appointment.date >= tomorrow,
                Appointment.date <= next_week,
            )
            .all()
        )
        availability_dates = {d[0] for d in availability_dates_query}
        week_dates = [tomorrow + timedelta(days=i) for i in range(7)]
        unconfigured_dates = [str(d) for d in week_dates if d not in availability_dates]

        return {
            "doc_id": doc_id,
            "todays_appointments": todays_appointments,
            "upcoming_appointments": upcoming_appointments,
            "past_appointments": past_appointments,
            "assigned_patients": assigned_patients,
            "missing_dates": unconfigured_dates,
            "missing_availability_dates": unconfigured_dates,
        }, 200


class DoctorMonthlyReports(Resource):
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or str(current_user.role) != "2":
            return {"message": "Only doctor can access monthly reports"}, 403

        doctor_record = Doctor.query.filter_by(email=current_user.email).first()
        if not doctor_record:
            return {"message": "Doctor record not found"}, 404

        pattern = os.path.join("instance", "reports", "*", f"doctor_{doctor_record.id}_*.html")
        report_files = sorted(glob.glob(pattern), reverse=True)

        reports = []
        for path in report_files:
            filename = os.path.basename(path)
            month_label = filename.replace(f"doctor_{doctor_record.id}_", "").replace(".html", "")
            try:
                datetime.strptime(month_label, "%Y-%m")
            except ValueError:
                continue

            reports.append({
                "month": month_label,
                "filename": filename,
                "generated_at": datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
                "download_url": f"/doctor/monthly-reports/{month_label}/download",
            })

        return {"reports": reports}, 200

    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or str(current_user.role) != "2":
            return {"message": "Only doctor can export monthly reports"}, 403

        doctor_record = Doctor.query.filter_by(email=current_user.email).first()
        if not doctor_record:
            return {"message": "Doctor record not found"}, 404

        data = request.get_json() or {}
        month_label = str(data.get("month", "")).strip()
        if not month_label:
            first_of_current = date.today().replace(day=1)
            previous_month_date = first_of_current - timedelta(days=1)
            month_label = previous_month_date.strftime("%Y-%m")

        result = _build_doctor_monthly_report(doctor_record.id, month_label)
        if not result:
            return {"message": "Invalid month format. Use YYYY-MM"}, 400

        return {
            "message": "Monthly report generated",
            "month": month_label,
            "appointments": result["appointments"],
            "treatments": result["treatments"],
            "download_url": f"/doctor/monthly-reports/{month_label}/download",
        }, 201


class DoctorMonthlyReportDownload(Resource):
    @jwt_required()
    def get(self, month_label):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or str(current_user.role) != "2":
            return {"message": "Only doctor can download monthly reports"}, 403

        doctor_record = Doctor.query.filter_by(email=current_user.email).first()
        if not doctor_record:
            return {"message": "Doctor record not found"}, 404

        start_date, end_date = _month_window_from_label(month_label)
        if not start_date or not end_date:
            return {"message": "Invalid month format. Use YYYY-MM"}, 400

        report_path = os.path.join("instance", "reports", month_label, f"doctor_{doctor_record.id}_{month_label}.html")
        if not os.path.exists(report_path):
            return {"message": "Report not found for requested month"}, 404

        return send_file(report_path, as_attachment=True)


class UpdateAppointmentStatus(Resource):
    @jwt_required()
    def post(self, app_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or str(current_user.role) != "2":
            return {"message": "Only doctor can update appointment status"}, 403

        doctor_record = Doctor.query.filter_by(email=current_user.email).first()
        if not doctor_record:
            return {"message": "Doctor record not found"}, 404

        appointment = Appointment.query.get(app_id)
        if not appointment:
            return {"message": "Appointment not found"}, 404

        if appointment.doctor_id != doctor_record.id:
            return {"message": "You can update only your appointments"}, 403

        data = request.get_json() or {}
        new_status = str(data.get("status", "")).strip().title()
        allowed_statuses = {"Booked", "Completed", "Cancelled"}

        if new_status not in allowed_statuses:
            return {"message": "Invalid status"}, 400

        appointment.status = new_status
        db.session.commit()
        return {"message": "Appointment status updated"}, 200


class DoctorAddTreatment(Resource):
    @jwt_required()
    def post(self, booking_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or str(current_user.role) != "2":
            return {"message": "Only doctor can add treatment"}, 403

        doctor_record = Doctor.query.filter_by(email=current_user.email).first()
        if not doctor_record:
            return {"message": "Doctor record not found"}, 404

        appointment = Appointment.query.get(booking_id)
        if not appointment:
            return {"message": "Appointment not found"}, 404

        if appointment.doctor_id != doctor_record.id:
            return {"message": "You can add treatment only for your appointments"}, 403

        if not appointment.patient_id:
            return {"message": "Cannot add treatment for unbooked slot"}, 400

        data = request.get_json() or {}
        diagnosis = str(data.get("diagnosis", "")).strip()
        prescription = str(data.get("prescription", "")).strip()
        notes = str(data.get("notes", "")).strip()
        progress = str(data.get("progress", "")).strip()

        if not diagnosis or not prescription or not progress:
            return {"message": "Diagnosis, prescription and progress are required"}, 400

        treatment = Treatment.query.filter_by(appointment_id=booking_id).first()
        if treatment:
            treatment.diagnosis = diagnosis
            treatment.prescription = prescription
            treatment.notes = notes
            treatment.progress = progress
        else:
            treatment = Treatment(
                appointment_id=booking_id,
                diagnosis=diagnosis,
                prescription=prescription,
                notes=notes,
                progress=progress,
            )
            db.session.add(treatment)

        # Ensure treated appointments move out of active lists.
        appointment.status = "Completed"
        db.session.commit()
        return {"message": "Treatment saved successfully"}, 200


class DoctorPatientHistory(Resource):
    @jwt_required()
    def get(self, pat_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        if not current_user or str(current_user.role) != "2":
            return {"message": "Only doctor can view patient history"}, 403

        doctor_record = Doctor.query.filter_by(email=current_user.email).first()
        if not doctor_record:
            return {"message": "Doctor record not found"}, 404

        patient_record = Patient.query.get(pat_id)
        if not patient_record:
            return {"message": "Patient not found"}, 404

        # Doctor can only view history for patients associated with this doctor.
        assigned = Appointment.query.filter_by(
            doctor_id=doctor_record.id,
            patient_id=pat_id,
        ).first()
        if not assigned:
            return {"message": "You can view only your assigned patients"}, 403

        appointments = (
            Appointment.query
            .filter(
                Appointment.doctor_id == doctor_record.id,
                Appointment.patient_id == pat_id,
            )
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .all()
        )

        appointment_history = [
            {
                "App_id": a.id,
                "Date": str(a.date),
                "Time": str(a.time),
                "Status": a.status,
            }
            for a in appointments
        ]

        treatment_records = (
            db.session.query(Treatment, Appointment)
            .join(Appointment, Treatment.appointment_id == Appointment.id)
            .filter(
                Appointment.doctor_id == doctor_record.id,
                Appointment.patient_id == pat_id,
            )
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .all()
        )

        treatments = [
            {
                "Treatment_id": t.id,
                "Appointment_id": a.id,
                "Date": str(a.date),
                "Time": str(a.time),
                "Diagnosis": t.diagnosis,
                "Prescription": t.prescription,
                "Notes": t.notes,
                "Progress": t.progress,
            }
            for t, a in treatment_records
        ]

        return {
            "patient": {
                "Pat_id": patient_record.id,
                "Name": f"{patient_record.first_name} {patient_record.last_name}",
                "Email": patient_record.email,
            },
            "appointments": appointment_history,
            "treatments": treatments,
        }, 200


class DoctorManageSlots(Resource):
    @jwt_required()
    def get(self, doc_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()
        doctor_record = Doctor.query.filter_by(email=current_user.email).first() if current_user else None

        if not current_user or current_user.role != 2 or not doctor_record:
            return {"message": "Only doctor can access slots"}, 403

        if doctor_record.id != doc_id:
            return {"message": "Unauthorized doctor id"}, 403

        today = date.today()
        next_week = today + timedelta(days=7)

        slots_query = (
            Appointment.query
            .filter(
                Appointment.doctor_id == doc_id,
                Appointment.date >= today,
                Appointment.date <= next_week,
            )
            .order_by(Appointment.date, Appointment.time)
            .all()
        )

        slots = [
            {
                "App_id": a.id,
                "Date": str(a.date),
                "Time": a.time.strftime("%H:%M"),
                "Status": a.status,
            }
            for a in slots_query
        ]

        dates = [str(today + timedelta(days=i)) for i in range(8)]

        return {
            "doc_id": doc_id,
            "dates": dates,
            "time_options": list(SLOT_TIME_OBJECTS.keys()),
            "slot_labels": SLOT_LABELS,
            "slots": slots,
        }, 200

    @jwt_required()
    def post(self, doc_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()
        doctor_record = Doctor.query.filter_by(email=current_user.email).first() if current_user else None

        if not current_user or current_user.role != 2 or not doctor_record:
            return {"message": "Only doctor can manage slots"}, 403

        if doctor_record.id != doc_id:
            return {"message": "Unauthorized doctor id"}, 403

        data = request.get_json() or {}
        selected_slots = data.get("slots", [])

        if not isinstance(selected_slots, list):
            return {"message": "slots must be a list"}, 400

        created = 0
        for slot in selected_slots:
            slot_date = slot.get("date")
            slot_time = slot.get("time")

            if not slot_date or not slot_time:
                continue

            if slot_time not in SLOT_TIME_OBJECTS:
                continue

            try:
                slot_date_obj = datetime.strptime(slot_date, "%Y-%m-%d").date()
            except ValueError:
                continue

            existing = Appointment.query.filter_by(
                doctor_id=doc_id,
                date=slot_date_obj,
                time=SLOT_TIME_OBJECTS[slot_time],
            ).first()
            if existing:
                continue

            new_slot = Appointment(
                doctor_id=doc_id,
                patient_id=None,
                date=slot_date_obj,
                time=SLOT_TIME_OBJECTS[slot_time],
                status="Available",
            )
            db.session.add(new_slot)
            created += 1

        db.session.commit()
        return {"message": "Slots updated", "created": created}, 200


class DoctorCancelSlot(Resource):
    @jwt_required()
    def delete(self, slot_id):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()
        doctor_record = Doctor.query.filter_by(email=current_user.email).first() if current_user else None

        if not current_user or current_user.role != 2 or not doctor_record:
            return {"message": "Only doctor can cancel slots"}, 403

        slot = Appointment.query.get(slot_id)
        if not slot:
            return {"message": "Slot not found"}, 404

        if slot.doctor_id != doctor_record.id:
            return {"message": "You can cancel only your slots"}, 403

        if slot.status != "Available":
            return {"message": "Only available slots can be removed"}, 400

        db.session.delete(slot)
        db.session.commit()
        return {"message": "Slot removed"}, 200


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
        invalidate_cache("search:*")
        
        return {"message": "Doctor added successfully"}, 201

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
        invalidate_cache("search:*")
        
        return {"message": "Doctor updated successfully"}, 200

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

        doctor.blacklisted = "Y"
        db.session.commit()
        return {"message": "Doctor blacklisted successfully"}, 200

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

        
        doctor.blacklisted = "N"
        db.session.commit()
        return {"message": "Doctor removed from blacklist successfully"}, 200

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
        
        invalidate_cache("search:*")
        
        return {"message": "Patient updated successfully"}, 200

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

        
        patient.blacklisted = "Y"
        db.session.commit()
        return {"message": "Patient blacklisted successfully"}, 200

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

#api for searching doctors by name or department and search patient by name or email, only admin can access this route
class Search(Resource):
    @jwt_required()
    @cache_response(ttl=900, prefix='search', user_specific=True)
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

# all Api Routes
api.add_resource(AdminDashboard, "/admin/dashboard")
api.add_resource(PatientDashboard, "/patient/dashboard")
api.add_resource(DoctorDashboard, "/doctor/dashboard")
api.add_resource(Login, "/login")
api.add_resource(Signup, "/signup")
api.add_resource(AddDoctor, "/add_doctor")
api.add_resource(UpdateDoctor, "/update_doctor/<int:doctor_id>")
api.add_resource(GetDoctor, "/get_doctor/<int:doctor_id>")
api.add_resource(DeleteDoctor, "/delete_doctor/<int:doctor_id>")
api.add_resource(BlacklistDoctor, "/blacklist_doctor/<int:doctor_id>")
api.add_resource(RemoveBlacklistDoctor, "/remove_blacklist_doctor/<int:doctor_id>")
api.add_resource(UpdatePatient, "/update_patient/<int:patient_id>")
api.add_resource(GetPatient, "/get_patient/<int:patient_id>")
api.add_resource(RemoveBlacklistPatient, "/remove_blacklist_patient/<int:patient_id>")
api.add_resource(BlacklistPatient, "/blacklist_patient/<int:patient_id>")
api.add_resource(DeletePatient, "/delete_patient/<int:patient_id>")
api.add_resource(PatientAvailableSlots, "/patient/available-slots")
api.add_resource(PatientBookSlot, "/patient/book-slot/<int:slot_id>")
api.add_resource(PatientCancelAppointment, "/patient/cancel-slot/<int:booking_id>")
api.add_resource(PatientExportTreatmentHistory, "/patient/export-treatment-history")
api.add_resource(PatientExportTreatmentHistoryStatus, "/patient/export-treatment-history/<int:job_id>")
api.add_resource(PatientExportTreatmentHistoryDownload, "/patient/export-treatment-history/<int:job_id>/download")
api.add_resource(UpdateAppointmentStatus, "/update_status/<int:app_id>")
api.add_resource(DoctorAddTreatment, "/doctor/add-treatment/<int:booking_id>")
api.add_resource(DoctorPatientHistory, "/doctor/patient-history/<int:pat_id>")
api.add_resource(DoctorManageSlots, "/doctor/slots/<int:doc_id>")
api.add_resource(DoctorCancelSlot, "/doctor/slots/cancel/<int:slot_id>")
api.add_resource(DoctorMonthlyReports, "/doctor/monthly-reports")
api.add_resource(DoctorMonthlyReportDownload, "/doctor/monthly-reports/<string:month_label>/download")
api.add_resource(Search, "/search")
