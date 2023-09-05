# Use the official Apache Airflow image with Python 3.10
FROM apache/airflow:latest-python3.10

# Set the working directory in the container
WORKDIR /alexnet

# Copy the current directory contents into the container at /app
#COPY . /alexnet <-- copy only essential stuff

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Command to run your Python application
# Command goes here