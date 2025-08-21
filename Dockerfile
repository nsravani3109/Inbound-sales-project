FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for numpy/pandas compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Initialize DB and seed loads
RUN python init_db.py && python seed_loads.py

# Expose port
EXPOSE 8080

# Run app
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"]
