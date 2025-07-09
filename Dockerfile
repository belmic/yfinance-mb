FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости для pandas и lxml
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY yfinance_server.py .

# Запускаем сервер
CMD ["python", "yfinance_server.py"]