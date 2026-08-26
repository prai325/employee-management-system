from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "employee_management",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.tasks.email_tasks"
    ]
)