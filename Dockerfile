# syntax=docker/dockerfile:1
FROM python:3.13.5

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (including stat_1.py)
COPY . .

# Run your application
CMD ["python", "app/main.py"]
