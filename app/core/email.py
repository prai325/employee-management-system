import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_welcome_email(
        email: str,
        first_name: str
):
    message = EmailMessage()

    message["Subject"] = "Welcome to Employee Management System"
    message["From"] = (
        f"{settings.smtp_from_name} "
        f"<{settings.smtp_from_email}>"
    )
    message["to"] = email

    message.set_content(
        f"""
Hello {first_name},

Welcome to Employee Management System.

Your account has been created successfully.

You can now login using your registered email address.

Regards,
Employee Management System
"""
    )

    with smtplib.SMTP(
        settings.smtp_host,
        settings.smtp_port
    ) as server:
        server.starttls()
        server.login(
            settings.smtp_username,
            settings.smtp_password
        )
        server.send_message(message)