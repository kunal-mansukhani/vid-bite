# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    texlive \
    texlive-latex-extra \
    sox

# Create a non-root user
RUN useradd -m appuser

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Create a directory for the app user
RUN mkdir -p /home/appuser/app

# Copy the application to the new directory
COPY . /home/appuser/app

# Change ownership of the application files
RUN chown -R appuser:appuser /home/appuser/app

# Switch to the non-root user
USER appuser

# Set the working directory to the app user's directory
WORKDIR /home/appuser/app

# Run app.py when the container launches
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]