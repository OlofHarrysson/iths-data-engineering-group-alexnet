# Use the official Apache Airflow image with Python 3.10
FROM apache/airflow:latest-python3.10

# Set the working directory in the container
WORKDIR /alexnet

# Switch back to the airflow user
USER airflow

# Copy requirements.txt into the container
COPY requirements.txt /alexnet/

# Remove editable installations from requirements.txt and install dependencies
RUN grep -v "^-e" /alexnet/requirements.txt > /alexnet/requirements_without_editable_install.txt && \
    pip install -r /alexnet/requirements_without_editable_install.txt

# Switch to root user for system-level installations
USER root

# Update package lists and install Git
RUN apt-get update && apt-get install -y git

# Create the /alexnet directory and set permissions
RUN mkdir -p /alexnet && chown airflow: /alexnet

# Copy test directory into the container
COPY tests /alexnet/

# CI/CD Steps
RUN echo "Running CI/CD"

# Initialize Git repository within /alexnet directory
RUN echo "Initializing Git repository" && \
    cd /alexnet && \
    git init && \
    echo "Installing pre-commit hooks" && \
    pre-commit install

# Run pytest
RUN echo "Running pytest" && \
    python -m pytest

RUN echo "CI/CD finished"

# Deactivate any virtual environment (if activated)
RUN deactivate

# Command to run your Python application (replace "main.py" with your actual entry point script)
CMD ["python", "main.py"]
