# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Copy pyproject.toml and requirements files
COPY pyproject.toml requirements.txt ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY . .

# Create directory for logs and data
RUN mkdir -p /app/logs /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port (if needed for health checks)
EXPOSE 8080

# Run the application using uv
CMD ["uv", "run", "python", "main.py"]
