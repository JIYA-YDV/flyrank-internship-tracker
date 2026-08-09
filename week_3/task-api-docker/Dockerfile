# Dockerfile
# ─────────────────────────────────────────────────────────────────
# Instructions for building the FastAPI app container image
# ─────────────────────────────────────────────────────────────────

# Start from official Python 3.11 image (slim = smaller size)
FROM python:3.11-slim

# Set the working directory inside the container
# All commands after this run from /code
WORKDIR /code

# ── Copy requirements FIRST (Docker layer caching optimization) ──
# If requirements.txt has not changed, Docker skips the pip install
# This makes rebuilds much faster when you only change app code
COPY requirements.txt .

# Install all Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy the app code ──────────────────────────────────────────
# This runs every time any code file changes
COPY ./app ./app

# Tell Docker the app listens on port 8000
EXPOSE 8000

# Command to run when the container starts
# --host 0.0.0.0  means accept connections from outside the container
# --reload        means restart when code files change (good for development)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]