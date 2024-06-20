FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run"]
