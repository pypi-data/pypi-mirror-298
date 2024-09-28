FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

RUN  apt-get update && apt-get install -y git

# Install the specific version of mantle-sdk
RUN pip install mantlebio==1.0.7