FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application code
COPY sienge_mcp/ ./sienge_mcp/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "sienge_mcp.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
