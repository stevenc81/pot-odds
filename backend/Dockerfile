# Single stage build to avoid path issues
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy all application files
COPY . .

# Create virtual environment and install dependencies
RUN uv venv && uv sync --frozen

# Expose port
EXPOSE 8000

# Run the application using the venv python
CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]