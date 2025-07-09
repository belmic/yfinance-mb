FROM python:3.11-slim

WORKDIR /app

# Устанавливаем Flask и CORS
RUN pip install --no-cache-dir \
    Flask==3.0.0 \
    flask-cors==4.0.0

# Копируем приложение
COPY app.py .

# Запускаем Flask
CMD ["python", "app.py"]