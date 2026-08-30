import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_email(
        to_email: str,
        subject: str,
        html_content: str
):
    message = EmailMessage()

    # message["From"] = settings.smtp_from_email
    message["From"] = (
            f"{settings.smtp_from_name} "
            f"<{settings.smtp_from_email}>"
        )
    message["to"] = to_email
    message["Subject"] = subject

    message.set_content(
        "Please open this email in an HTML-compatible email client."
    )
    message.add_alternative(
        html_content,
        subtype="html"
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