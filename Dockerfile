FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Railway автоматически устанавливает PORT
EXPOSE ${PORT:-8000}

# Используем gunicorn для production
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 60 server:app