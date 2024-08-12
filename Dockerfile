# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install dependencies - most frequent updated file(s)
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app     
ENV FLASK_DEBUG=False

# Run the application. By default uses IP: 127.0.0.1. Specify current host (0.0.0.0) and port
#
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
