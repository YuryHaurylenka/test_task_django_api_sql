FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
