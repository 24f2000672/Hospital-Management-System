import os
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def _as_bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def is_valid_email(value):
    if not value:
        return False
    return EMAIL_REGEX.fullmatch(str(value).strip()) is not None


def send_email(subject, html_body, to_email, text_body=None):
    if not is_valid_email(to_email):
        print(f"[EMAIL] Skipping send. Invalid recipient email: {to_email}")
        return False

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_user or "noreply@hospital.local")

    use_tls = _as_bool(os.getenv("SMTP_USE_TLS", "true"), default=True)
    use_ssl = _as_bool(os.getenv("SMTP_USE_SSL", "false"), default=False)

    if not smtp_host:
        print("[EMAIL] SMTP_HOST is not set. Skipping email send.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    if text_body:
        msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
            server.ehlo()
            if use_tls:
                server.starttls()
                server.ehlo()

        if smtp_user and smtp_password:
            server.login(smtp_user, smtp_password)

        server.sendmail(from_email, [to_email], msg.as_string())
        server.quit()
        print(f"[EMAIL] Sent to {to_email} | {subject}")
        return True
    except Exception as exc:
        print(f"[EMAIL] Failed for {to_email}: {exc}")
        return False
