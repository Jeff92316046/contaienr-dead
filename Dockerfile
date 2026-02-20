# Use minimal Alpine Linux based Python 3.13 image
FROM python:3.13-alpine

# Use Astral's uv for fast and lightweight python dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency definition files
COPY pyproject.toml .

# Install dependencies into system Python directly (since we are in a container)
# This keeps the image extremely small
RUN uv pip install --system requests docker

# Copy our script
COPY main.py .

# Standard command to run the watcher
CMD ["python", "-u", "main.py"]
