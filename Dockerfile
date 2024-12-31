FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PORT=8080

# Run the application with Gunicorn
CMD exec gunicorn --bind :$PORT main:app