# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml ./
COPY README.md ./

# Install Python dependencies
RUN pip install -e ".[dev]"

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/
COPY data/ ./data/
COPY archive/ ./archive/

# Create output directory
RUN mkdir -p data/output

# Run tests to verify setup
RUN python -m pytest tests/ -v

# Set default command
CMD ["python", "src/main.py"]

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import src.main; print('OK')" || exit 1
