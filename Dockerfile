FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir \
    Flask==3.0.0 \
    flask-cors==4.0.0 \
    gunicorn==21.2.0

# Копируем файлы
COPY server.py .
COPY start.sh .

# Делаем скрипт исполняемым
RUN chmod +x start.sh

# Запускаем через скрипт
CMD ["./start.sh"]