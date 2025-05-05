# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt /app/requirements.txt

# Install system dependencies for Pyxel
RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx \
  libx11-xcb1 \
  libxcb-dri3-0 \
  libxrender1 \
  libxrandr2 \
  libxi6 \
  libxcursor1 \
  libxinerama1 \
  libxxf86vm1 \
  libsdl2-2.0-0 \
  libsdl2-image-2.0-0 \
  libsdl2-mixer-2.0-0 \
  libsdl2-ttf-2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the application
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
