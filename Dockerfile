# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install SQLite
RUN apt-get update && \
    apt-get install -y sqlite3 libsqlite3-dev

# Set the working directory in the container
WORKDIR /app

# Copy your application files
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to allow external connections
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
