# Use the desired Python base image
FROM python:3.10.12-slim-bullseye

# Set the working directory
WORKDIR /main

# Copy the requirements file
COPY requirements.txt requirements.txt

# Upgrade pip to a specific version
RUN python3 -m venv venv && \
    /app/venv/bin/pip install --upgrade pip==21.3.1

# Set the PATH to include the virtual environment
ENV PATH="/main/venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev cmake libcurl4-openssl-dev nodejs screen

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set executable permissions for your scripts (if needed)
RUN chmod +x ./main.py
RUN chmod +x ./start.sh

# Avoid using chmod -R 777; instead, set appropriate permissions as needed
# For example, if you have a data directory, you can do:
# RUN chmod -R 755 /app/data

# Define the command to run your application
CMD ["screen", "-d", "-m", "python3", "check.py"]
CMD ["uvicorn", "main:main", "--host", "0.0.0.0", "--port", "7860"]
