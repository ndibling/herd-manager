# syntax=docker/dockerfile:1.7
FROM python:3.11-slim
WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

# Optionally mount host ./data into /tmp/data at build time; if present, copy it
RUN --mount=type=bind,source=data,target=/tmp/data,optional=true \
    if [ -d /tmp/data ]; then cp -a /tmp/data /srv/data; else mkdir -p /srv/data; fi

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
