# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Initialize database and seed loads
RUN python init_db.py && python seed_loads.py

# Expose the port (optional, Cloud Run uses $PORT)
EXPOSE 8080

# Run FastAPI with dynamic port from Cloud Run
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"]