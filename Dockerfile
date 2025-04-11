# Use an official Python runtime as a parent image (with slim variant for a smaller image)
FROM python:3.9-slim

# Install nmap and other OS-level dependencies
RUN apt-get update && \
    apt-get install -y nmap && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt and install any Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /app
COPY . .

# Set the start command to run your bot
CMD ["python", "bot.py"]
