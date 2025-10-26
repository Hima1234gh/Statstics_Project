# syntax=docker/dockerfile:1

FROM python:3.13.5

# Set working directory
WORKDIR /app

# Copy dependency file and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run your application
CMD ["python", "main.py"]
