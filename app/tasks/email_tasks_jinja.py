from app.core.celery_app import celery_app
from app.core.welcome_email import send_welcome_email

@celery_app.task
def send_welcome_email_task(
    email: str,
    first_name: str
):
    send_welcome_email(
        email=email,
        first_name=first_name
    )
#send_welcome_email_task() is a Celery task.