# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm -rf ~/.cache/pip

# Copy project
COPY . .

# Create directories for static and media files
RUN mkdir -p /app/static /app/media

# Copy and set up entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create a non-root user and adjust permissions
RUN useradd -m appuser && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Run migrations, collectstatic, then start Gunicorn
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command: start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "id_maker.wsgi:application"]
