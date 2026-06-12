# Use a slim, secure official Python runtime base
FROM python:3.11-slim

# Set an isolated execution directory context inside the container
WORKDIR /app

# Copy dependency structures and install required packages
RUN pip install --no-cache-dir websockets redis

# Copy the server engine code into the container filesystem image
COPY server.py .

# Inform Docker that the engine listens on network port 8765
EXPOSE 8765

# Launch the server application when the container starts
CMD ["python", "server.py"]

