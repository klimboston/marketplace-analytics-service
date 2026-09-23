from celery import Celery

from src.marketplace_analytics_service.core.config import settings

celery_app = Celery(
    "marketplace_tasks", broker=settings.redis_url, backend=settings.redis_url
)

celery_app.autodiscover_tasks(["src.marketplace_analytics_service"])
