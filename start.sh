#!/bin/bash
# start.sh

# Проверяем, установлен ли PORT
if [ -z "$PORT" ]; then
    echo "PORT not set, using 8000"
    export PORT=8000
fi

echo "Starting server on port $PORT"

# Запускаем gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 --log-level info server:app