FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-opencv \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application files
COPY . .

# Create directories for mounted volumes
RUN mkdir -p videos output

CMD ["python3", "main.py"]