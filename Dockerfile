FROM python:3.11

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Предоставляем права на выполнение скрипту celery.sh
RUN chmod +x /booking/docker/celery.sh
RUN chmod +x /booking/docker/app.sh

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

