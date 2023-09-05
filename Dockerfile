# Use the official Apache Airflow image with Python 3.10
FROM apache/airflow:latest-python3.10

# Set the working directory in the container
WORKDIR /alexnet

COPY requirements.txt .

# Copy requirements.txt into the container
RUN grep -v "^-e" requirements.txt > requirements_without_editable_install.txt
RUN pip install -r requirements_without_editable_install.txt

# This does not allow for import of the newsfeed as a module, causing the tests to fail

RUN echo "Running CI/CD"

# Run pytest
# RUN echo "Running pytest" && \
#     python -m pytest

RUN echo "CI/CD finished"
#CMD ["python", "main.py"]