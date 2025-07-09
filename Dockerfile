FROM python:3.11-slim
WORKDIR /app
COPY test_server.py .
CMD ["python", "test_server.py"]