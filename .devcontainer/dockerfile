# syntax=docker/dockerfile:1   # Specifies Dockerfile version to use. In this case, version 1.

FROM python:3.9-slim-buster   # Defines the base image to use for your Docker image. Here, it's the slim-buster version of the official Python 3.9 image.

WORKDIR /app   # Sets the working directory in the Docker container. Any command that follows in the Dockerfile will be run in this directory.

COPY requirements.txt .  # Copies the requirements.txt file from your project to the working directory in the Docker image.

RUN pip install -r requirements.txt  # Runs pip install command in your Docker image to install Python dependencies listed in your requirements.txt file.

COPY . .  # Copies everything else in your project (denoted by '.') to the working directory in the Docker image.
