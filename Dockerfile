# This Dockerfile builds a lightweight Python image with FastAPI and Uvicorn
# using the tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim base image.

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim AS builder

# Create a working directory for the application code.
WORKDIR /code/app

# Copy the requirements.txt file into the working directory.
COPY ./requirements.txt /code/requirements.txt

# Install the Python requirements using a pip cache mount.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /code/requirements.txt

# Copy the application code into the working directory.
COPY . /code/app

# Expose port 80 for the application to listen on.
EXPOSE 80

# Start the Uvicorn server to run the FastAPI application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]