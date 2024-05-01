FROM python:3.12.3-alpine3.19

# Install necessary packages
RUN apk add --no-cache \
    nodejs \
    npm \
    git

# Set working directory
WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY package*.json ./
RUN npm install