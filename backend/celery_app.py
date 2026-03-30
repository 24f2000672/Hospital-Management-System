import os
from celery import Celery
from celery.schedules import crontab
from app import create_app


flask_app = create_app()

# Bind SQLAlchemy/JWT/api to this app instance for worker/beat processes.
import models
from flask_jwt_extended import JWTManager
from routes import api

models.db.init_app(flask_app)
JWTManager(flask_app)
api.init_app(flask_app)

daily_reminder_hour = int(os.getenv("DAILY_REMINDER_HOUR", "8"))
daily_reminder_minute = int(os.getenv("DAILY_REMINDER_MINUTE", "0"))

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/1"),
    include=["tasks"],
)

celery_app.conf.update(
    timezone=os.getenv("CELERY_TIMEZONE", "Asia/Kolkata"),
    enable_utc=False,
)

celery_app.conf.beat_schedule = {
    "daily-same-day-appointment-reminder": {
        "task": "tasks.send_same_day_appointment_reminders",
        "schedule": crontab(hour=daily_reminder_hour, minute=daily_reminder_minute),
    },
    "monthly-doctor-report-job": {
        "task": "tasks.generate_monthly_doctor_reports",
        "schedule": crontab(day_of_month=1, hour=2, minute=0),
    },
}


class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = ContextTask

# Backward compatibility for existing command: celery -A celery_app.celery ...
celery = celery_app
