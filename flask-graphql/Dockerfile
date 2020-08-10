FROM python:3.6-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a working directory for the flask project
WORKDIR /usr/src/app

# Copy requirements to the container
COPY Pipfile Pipfile.lock /usr/src/app/

# Install the requirements to the container
RUN pip install pipenv && pipenv install --system

# Copy the project files into the working directory
COPY . /usr/src/app/
