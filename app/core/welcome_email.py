import smtplib
from email.message import EmailMessage
from app.core.config import settings
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from app.core.email_service import send_email

BASE_DIR = Path(__file__).resolve().parent.parent

env = Environment(
    loader=FileSystemLoader(
        BASE_DIR / "templates" / "emails"
    )
)

def send_welcome_email(
        email: str,
        first_name: str
):
    template = env.get_template(
        "welcome_email.html"
    )

    html_content = template.render(
        first_name = first_name
    )

    send_email(
        to_email=email,
        subject="Welcome to Employee Management System",
        html_content=html_content
    )