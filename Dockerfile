# Use the official Apache Airflow image with Python 3.10
FROM apache/airflow:latest-python3.10

# Set the working directory in the container
WORKDIR /alexnet

COPY requirements.txt .

# Copy data_lake and data_warehouse
COPY data .

# Copy requirements.txt into the container
RUN grep -v "^-e" requirements.txt > requirements_without_editable_install.txt
RUN pip install -r requirements_without_editable_install.txt

RUN echo "Finished"

#CMD ["python", "main.py"]
