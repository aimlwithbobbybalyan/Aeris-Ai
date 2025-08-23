# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your app runs on (e.g., 8000)
EXPOSE 8000

# Command to run your app (adjust for your actual run command)
# Example: For Flask app named app.py
CMD ["python", "app.py"]
