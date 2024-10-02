# Use an official Python runtime as a parent image
FROM python

# Set the working directory in the container
WORKDIR /app

# Copy the directory contents into the container
COPY . /app
COPY .. /worker_nodes/app

# Install any needed packages
RUN pip install -r requirements.txt

# Expose the port for the FastAPI server
EXPOSE 8000
