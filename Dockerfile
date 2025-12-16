FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .
RUN chmod +x /app/entrypoint.sh

RUN ls -l /app

ENTRYPOINT ["/app/entrypoint.sh"]
