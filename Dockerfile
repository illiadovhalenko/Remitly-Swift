FROM python:3.9-slim

WORKDIR /SwiftRemitly

# Install system dependencies first
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use the full path to uvicorn or the module execution method
CMD ["python", "-m", "uvicorn", "app.main:app_main", "--host", "0.0.0.0", "--port", "8080"]