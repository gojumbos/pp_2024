# Use an official Ubuntu base image
FROM python

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the Flask app files to the working directory
COPY . /app

# Expose port 8000 for the Flask app
EXPOSE 8000

# Command to run the Gunicorn server
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "app:app"]
