FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy only requirements to cache them in docker layer
COPY requirements.txt .
# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user first
RUN useradd -m -u 1000 botuser

# Copy application code and set ownership
COPY --chown=botuser:botuser . .

# Create directory for logs with correct ownership
RUN mkdir -p /app/logs && \
    chown -R botuser:botuser /app/logs && \
    chmod 755 /app/logs

USER botuser

CMD ["python", "bot.py"]