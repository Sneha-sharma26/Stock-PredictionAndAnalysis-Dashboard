# Use official lightweight Python image
FROM python:3.10-slim-bullseye
# or even
FROM python:3.10-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files into the container
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port for Render (or use PORT env)
EXPOSE 10000

# Set environment variable for Streamlit (optional but clean)
ENV PYTHONUNBUFFERED=1

# Run Streamlit app (Render will bind to PORT env variable or default 10000)
CMD ["streamlit", "run", "src/app.py", "--server.port=10000", "--server.address=0.0.0.0"]
