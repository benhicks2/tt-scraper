# syntax=docker.io/docker/dockerfile:1

FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:5000/health || exit 1

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
