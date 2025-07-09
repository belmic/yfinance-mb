FROM python:3.11-slim

WORKDIR /app

# Устанавливаем базовые зависимости
RUN pip install --no-cache-dir \
    Flask==3.0.0 \
    flask-cors==4.0.0 \
    gunicorn==21.2.0

# Копируем файл сервера
COPY server.py .

# НЕ используем EXPOSE с переменной
# Railway сам управляет портами

# Запускаем через python для начала
CMD ["python", "server.py"]