# server.py
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import yfinance as yf
from yfinance_handler import YFinanceHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для n8n

# Инициализируем обработчик
yf_handler = YFinanceHandler()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint для Railway"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "yfinance-mcp"
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Корневой endpoint с информацией о сервисе"""
    return jsonify({
        "service": "YFinance MCP Server",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/api/stock": "Get stock data",
            "/api/history": "Get historical data",
            "/api/info": "Get company info",
            "/api/news": "Get stock news"
        }
    }), 200

@app.route('/api/stock', methods=['POST'])
def get_stock():
    """Получить текущие данные по акции"""
    try:
        data = request.json
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        
        result = yf_handler.get_current_price(symbol)
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting stock data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['POST'])
def get_history():
    """Получить исторические данные"""
    try:
        data = request.json
        symbol = data.get('symbol')
        period = data.get('period', '1mo')  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval = data.get('interval', '1d')  # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        
        result = yf_handler.get_historical_data(symbol, period, interval)
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting historical data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/info', methods=['POST'])
def get_info():
    """Получить информацию о компании"""
    try:
        data = request.json
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        
        result = yf_handler.get_company_info(symbol)
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting company info: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/news', methods=['POST'])
def get_news():
    """Получить новости по акции"""
    try:
        data = request.json
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        
        result = yf_handler.get_news(symbol)
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting news: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting YFinance MCP Server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)