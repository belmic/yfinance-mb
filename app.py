# app.py
import os
import sys
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Создаем Flask app
app = Flask(__name__)
CORS(app)

# Печатаем информацию при старте
logger.info("Starting Flask application")
logger.info(f"PORT from environment: {os.environ.get('PORT', 'NOT SET')}")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "yfinance-api"
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "service": "YFinance API Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/health",
            "/api/test",
            "/api/stock"
        ]
    }), 200

@app.route('/api/test', methods=['GET', 'POST'])
def test():
    """Test endpoint"""
    return jsonify({
        "message": "API is working",
        "method": request.method,
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/stock', methods=['POST'])
def get_stock():
    """Basic stock endpoint - пока без yfinance"""
    try:
        data = request.json or {}
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        
        # Пока возвращаем тестовые данные
        return jsonify({
            "success": True,
            "symbol": symbol,
            "message": "Stock endpoint is working (test data)",
            "data": {
                "price": 100.00,
                "name": f"Test Company {symbol}"
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_stock: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Получаем порт
    port_str = os.environ.get('PORT', '8000')
    port = int(port_str)
    
    logger.info(f"Starting Flask server on port {port}")
    
    # Запускаем сервер
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )