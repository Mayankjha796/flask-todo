# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install required packages directly
RUN pip install --no-cache-dir Flask Flask-SQLAlchemy

# Copy application code
COPY . .

# Expose default Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]


