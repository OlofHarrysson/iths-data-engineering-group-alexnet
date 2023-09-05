# Use the official Apache Airflow image with Python 3.10
FROM apache/airflow:latest-python3.10

# Set the working directory in the container
WORKDIR /alexnet

# Copy the current directory contents into the container at /app
COPY /data /alexnet/
COPY requirements.txt /alexnet/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip -e

# CI/CD HERE

# Command to run your Python application