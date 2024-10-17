# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install ping or fping
RUN apt-get update && apt-get install -y inetutils-ping

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask
EXPOSE 5000

# Run the Flask app using gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
