# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Command to run your bot
CMD ["python", "auth_users.py"]
