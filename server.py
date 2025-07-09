# server.py
import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    logger.info("Health check called")
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "port": os.environ.get('PORT', 'not set')
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "service": "YFinance MCP Server",
        "status": "running",
        "environment": {
            "PORT": os.environ.get('PORT', 'not set'),
            "RAILWAY_ENVIRONMENT": os.environ.get('RAILWAY_ENVIRONMENT', 'not set')
        }
    }), 200

@app.route('/api/test', methods=['GET', 'POST'])
def test():
    """Test endpoint"""
    return jsonify({
        "message": "Test successful",
        "method": request.method
    }), 200

if __name__ == '__main__':
    # Получаем порт из переменной окружения
    port_str = os.environ.get('PORT', '8000')
    
    try:
        port = int(port_str)
    except ValueError:
        logger.error(f"Invalid PORT value: {port_str}")
        port = 8000
    
    logger.info(f"Starting server on port {port}")
    logger.info(f"Environment PORT: {os.environ.get('PORT', 'NOT SET')}")
    
    # Запускаем сервер
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)