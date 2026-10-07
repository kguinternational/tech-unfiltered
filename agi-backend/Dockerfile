FROM python:3.11-slim

# Install system dependencies required for building ML packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Whisper requires git to install directly from the repo sometimes, but we can just use pip install openai-whisper
RUN pip install --no-cache-dir openai-whisper

# Copy the rest of the application
COPY . .

CMD ["python", "main.py"]
