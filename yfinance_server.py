# yfinance_server.py
import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import yfinance as yf

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

logger.info("YFinance server starting...")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "service": "YFinance API Server",
        "version": "1.0.1",
        "status": "running",
        "yfinance_version": yf.__version__
    }), 200

@app.route('/api/stock', methods=['POST'])
def get_stock():
    """Get stock information"""
    try:
        data = request.json or {}
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        
        logger.info(f"Fetching data for symbol: {symbol}")
        
        # Получаем данные через yfinance
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Базовая информация
        result = {
            "success": True,
            "symbol": symbol,
            "data": {
                "price": info.get('currentPrice', info.get('regularMarketPrice')),
                "previousClose": info.get('previousClose'),
                "marketCap": info.get('marketCap'),
                "name": info.get('longName', info.get('shortName')),
                "currency": info.get('currency'),
                "exchange": info.get('exchange')
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error fetching stock data: {str(e)}")
        return jsonify({
            "error": str(e),
            "symbol": symbol
        }), 500

@app.route('/api/history', methods=['POST'])
def get_history():
    """Get historical data"""
    try:
        data = request.json or {}
        symbol = data.get('symbol')
        period = data.get('period', '1mo')
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        
        logger.info(f"Fetching history for {symbol}, period: {period}")
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        # Конвертируем в список
        history_data = []
        for index, row in hist.iterrows():
            history_data.append({
                "date": index.strftime('%Y-%m-%d'),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2),
                "low": round(row['Low'], 2),
                "close": round(row['Close'], 2),
                "volume": int(row['Volume'])
            })
        
        return jsonify({
            "success": True,
            "symbol": symbol,
            "period": period,
            "data": history_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/financials', methods=['POST'])
def get_financials():
    """Get financial statements"""
    try:
        data = request.json or {}
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        
        logger.info(f"Fetching financials for {symbol}")
        
        ticker = yf.Ticker(symbol)
        
        # Получаем финансовые данные
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        cash_flow = ticker.cashflow
        
        # Конвертируем первую колонку каждого отчета
        result = {
            "success": True,
            "symbol": symbol,
            "data": {
                "income_statement": {},
                "balance_sheet": {},
                "cash_flow": {}
            }
        }
        
        # Income Statement
        if financials is not None and not financials.empty:
            latest_date = financials.columns[0]
            for idx in financials.index:
                result["data"]["income_statement"][idx] = float(financials.loc[idx, latest_date]) if not pd.isna(financials.loc[idx, latest_date]) else None
        
        # Balance Sheet
        if balance_sheet is not None and not balance_sheet.empty:
            latest_date = balance_sheet.columns[0]
            for idx in balance_sheet.index:
                result["data"]["balance_sheet"][idx] = float(balance_sheet.loc[idx, latest_date]) if not pd.isna(balance_sheet.loc[idx, latest_date]) else None
        
        # Cash Flow
        if cash_flow is not None and not cash_flow.empty:
            latest_date = cash_flow.columns[0]
            for idx in cash_flow.index:
                result["data"]["cash_flow"][idx] = float(cash_flow.loc[idx, latest_date]) if not pd.isna(cash_flow.loc[idx, latest_date]) else None
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error fetching financials: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Добавим pandas для financials
    import pandas as pd
    
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting YFinance server on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )