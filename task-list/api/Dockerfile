# Use the official Python image as the base image
FROM python:3.9-slim

# Install development packages for building Python packages
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files from the current directory to the container
COPY . .

# Expose the port on which the FastAPI app will run
EXPOSE 8000

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

