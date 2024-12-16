from pathlib import Path

from PIL import Image
from celery import Celery
from app.config import settings

celery = Celery('tasks', broker=settings.REDIS_URL)
celery.conf.broker_connection_retry_on_startup = True

@celery.task
def add(x, y):
    return x + y


@celery.task
def process_image(path: str):
    path = Path(path)
    image = Image.open(path)
    image_resize = image.resize((200, 200))
    image_resize.save(f"app/static/images/small/small_{path.name}")