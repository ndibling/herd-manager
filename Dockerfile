FROM python:3.11-slim

WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

# OPTIONAL DATA DIRECTORY — safe for GitHub Actions
COPY data/ data/ || true

RUN if [ -d "data" ]; then \
        cp -a data /srv/data; \
    else \
        mkdir -p /srv/data; \
    fi

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
