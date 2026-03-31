import csv
import os
from datetime import date, datetime, timedelta
from collections import Counter
from sqlalchemy import and_

from celery_app import celery
from models import db, Appointment, Doctor, Patient, Treatment, ExportJob, NotificationLog
from mail import send_email, is_valid_email


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _log_notification(recipient, channel, subject, message):
    entry = NotificationLog(
        recipient=recipient,
        channel=channel,
        subject=subject,
        message=message,
    )
    db.session.add(entry)
    db.session.commit()
    print(f"[{channel.upper()}] to {recipient} | {subject or 'Notification'} | {message}")


def _month_window_for_previous_month(ref_date=None):
    ref_date = ref_date or date.today()
    first_of_current = ref_date.replace(day=1)
    last_of_previous = first_of_current - timedelta(days=1)
    first_of_previous = last_of_previous.replace(day=1)
    return first_of_previous, first_of_current


@celery.task(name="tasks.send_same_day_appointment_reminders")
def send_same_day_appointment_reminders():
    today = date.today()
    reminder_days_ahead = int(os.getenv("REMINDER_DAYS_AHEAD", "1"))
    target_date = today + timedelta(days=reminder_days_ahead)

    booked = (
        db.session.query(Appointment, Doctor, Patient)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .join(Patient, Appointment.patient_id == Patient.id)
        .filter(
            and_(
                Appointment.date == target_date,
                Appointment.status == "Booked",
                Appointment.patient_id.isnot(None),
            )
        )
        .order_by(Appointment.time)
        .all()
    )

    count = 0
    emails_sent = 0
    emails_failed = 0
    skipped_invalid_emails = 0
    for appointment, doctor, patient in booked:
        day_text = "today" if reminder_days_ahead == 0 else f"on {appointment.date}"
        msg = (
            f"Reminder: You have an appointment {day_text} at {appointment.time.strftime('%H:%M')} "
            f"with Dr. {doctor.first_name} {doctor.last_name}."
        )

        # Channel placeholders: wire real providers here (SMTP/GChat webhook/SMS gateway).
        valid_email = is_valid_email(patient.email)
        if valid_email:
            email_sent = send_email("Appointment Reminder", f"<p>{msg}</p>", patient.email, msg)
            if email_sent:
                _log_notification(patient.email, "email", "Appointment Reminder", msg)
                emails_sent += 1
            else:
                emails_failed += 1
        elif patient.email:
            skipped_invalid_emails += 1
            print(
                f"[EMAIL] Skipping patient_id={patient.id}. Invalid email value: {patient.email}"
            )
        if patient.phone:
            _log_notification(patient.phone, "sms", "Appointment Reminder", msg)
        if valid_email:
            _log_notification(patient.email, "gchat", "Appointment Reminder", msg)
        count += 1

    return {
        "run_date": str(today),
        "target_appointment_date": str(target_date),
        "reminder_days_ahead": reminder_days_ahead,
        "patients_notified": count,
        "emails_sent": emails_sent,
        "emails_failed": emails_failed,
        "invalid_emails_skipped": skipped_invalid_emails,
    }


@celery.task(name="tasks.generate_monthly_doctor_reports")
def generate_monthly_doctor_reports():
    # Doctor-only monthly reporting job.
    start_date, end_date = _month_window_for_previous_month()
    month_label = start_date.strftime("%Y-%m")

    reports_root = os.path.join("instance", "reports", month_label)
    _ensure_dir(reports_root)

    doctors = Doctor.query.all()
    generated = 0
    doctors_notified = 0

    for doctor in doctors:
        appointments = (
            Appointment.query.filter(
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

        report_path = os.path.join(reports_root, f"doctor_{doctor.id}_{month_label}.html")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("<html><head><title>Monthly Doctor Report</title></head><body>")
            f.write(f"<h1>Monthly Report - {month_label}</h1>")
            f.write(f"<h2>Doctor: {doctor.first_name} {doctor.last_name}</h2>")
            f.write(f"<p>Total appointments: {len(appointments)}</p>")
            f.write(f"<p>Total treatments: {len(treatments)}</p>")

            f.write("<h3>Diagnosis Summary</h3><ul>")
            if diagnosis_counts:
                for diagnosis, count in diagnosis_counts.items():
                    f.write(f"<li>{diagnosis}: {count}</li>")
            else:
                f.write("<li>No diagnosis records in this month.</li>")
            f.write("</ul>")

            f.write("<h3>Appointments</h3><table border='1' cellpadding='6'>")
            f.write("<tr><th>ID</th><th>Date</th><th>Time</th><th>Status</th></tr>")
            for a in appointments:
                f.write(
                    f"<tr><td>{a.id}</td><td>{a.date}</td><td>{a.time}</td><td>{a.status}</td></tr>"
                )
            f.write("</table>")
            f.write("</body></html>")

        if doctor.email:
            email_body = (
                f"<p>Your monthly report for <strong>{month_label}</strong> is ready.</p>"
                f"<p>Report path: {report_path}</p>"
            )
            email_sent = send_email(
                f"Monthly report generated ({month_label})",
                email_body,
                doctor.email,
                f"Your monthly report is ready: {report_path}",
            )
            if email_sent:
                _log_notification(
                    doctor.email,
                    "email",
                    f"Monthly report generated ({month_label})",
                    f"Report ready at: {report_path}",
                )
                doctors_notified += 1
        generated += 1

    return {
        "audience": "doctors",
        "month": month_label,
        "doctors_processed": generated,
        "doctors_notified": doctors_notified,
        "report_dir": reports_root,
    }


@celery.task(name="tasks.export_treatment_history_csv")
def export_treatment_history_csv(export_job_id):
    job = ExportJob.query.get(export_job_id)
    if not job:
        return {"error": "Export job not found"}

    try:
        job.status = "RUNNING"
        db.session.commit()

        patient = Patient.query.get(job.patient_id)
        if not patient:
            raise ValueError("Patient not found")

        treatments = (
            db.session.query(Treatment, Appointment, Doctor)
            .join(Appointment, Treatment.appointment_id == Appointment.id)
            .join(Doctor, Appointment.doctor_id == Doctor.id)
            .filter(Appointment.patient_id == job.patient_id)
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .all()
        )

        export_dir = os.path.join("instance", "exports")
        _ensure_dir(export_dir)
        filename = f"treatment_history_patient_{job.patient_id}_{int(datetime.utcnow().timestamp())}.csv"
        file_path = os.path.join(export_dir, filename)

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Treatment ID",
                "Appointment ID",
                "Date",
                "Time",
                "Doctor",
                "Diagnosis",
                "Prescription",
                "Progress",
                "Notes",
            ])
            for t, a, d in treatments:
                writer.writerow([
                    t.id,
                    a.id,
                    str(a.date),
                    str(a.time),
                    f"{d.first_name} {d.last_name}",
                    t.diagnosis or "",
                    t.prescription or "",
                    t.progress or "",
                    t.notes or "",
                ])

        job.status = "COMPLETED"
        job.file_path = file_path
        job.completed_at = datetime.utcnow()
        job.error_message = None
        db.session.commit()

        if patient.email:
            email_body = (
                "<p>Your treatment history export is completed.</p>"
                f"<p>Job ID: {job.id}</p>"
            )
            email_sent = send_email(
                "Treatment history export completed",
                email_body,
                patient.email,
                f"Your CSV export is ready. Job ID: {job.id}",
            )
            if email_sent:
                _log_notification(
                    patient.email,
                    "email",
                    "Treatment history export completed",
                    f"Your CSV export is ready. Job ID: {job.id}",
                )

        return {"job_id": job.id, "status": job.status, "file_path": file_path}
    except Exception as exc:
        job.status = "FAILED"
        job.error_message = str(exc)
        job.completed_at = datetime.utcnow()
        db.session.commit()
        return {"job_id": job.id, "status": job.status, "error": str(exc)}
