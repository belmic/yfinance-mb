# yfinance_handler.py
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import logging
import json

logger = logging.getLogger(__name__)

class YFinanceHandler:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 60  # секунды
    
    def get_ticker_info(self, symbol, period='1y'):
        """
        Получить полную финансовую информацию по тикеру
        
        Args:
            symbol: Тикер компании (например, 'AAPL')
            period: Период для исторических данных (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            Словарь со всей доступной финансовой информацией
        """
        try:
            ticker = yf.Ticker(symbol)
            
            # Собираем все данные
            result = {
                "success": True,
                "symbol": symbol,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "company_info": self._get_company_overview(ticker),
                    "current_trading": self._get_trading_info(ticker),
                    "financial_statements": self._get_financial_statements(ticker),
                    "key_metrics": self._get_key_metrics(ticker),
                    "earnings": self._get_earnings_data(ticker),
                    "dividends": self._get_dividends_data(ticker),
                    "analyst_recommendations": self._get_analyst_data(ticker),
                    "institutional_holders": self._get_institutional_data(ticker),
                    "historical_data": self._get_historical_prices(ticker, period),
                    "options": self._get_options_data(ticker),
                    "news": self._get_recent_news(ticker)
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching complete info for {symbol}: {str(e)}")
            return {"success": False, "error": str(e), "symbol": symbol}
    
    def _get_company_overview(self, ticker):
        """Базовая информация о компании"""
        try:
            info = ticker.info
            return {
                "name": info.get('longName', info.get('shortName')),
                "sector": info.get('sector'),
                "industry": info.get('industry'),
                "country": info.get('country'),
                "city": info.get('city'),
                "state": info.get('state'),
                "website": info.get('website'),
                "phone": info.get('phone'),
                "employees": info.get('fullTimeEmployees'),
                "description": info.get('longBusinessSummary'),
                "officers": self._get_company_officers(info)
            }
        except Exception as e:
            logger.error(f"Error in company overview: {str(e)}")
            return {}
    
    def _get_company_officers(self, info):
        """Информация о руководстве"""
        officers = []
        if 'companyOfficers' in info:
            for officer in info.get('companyOfficers', []):
                officers.append({
                    "name": officer.get('name'),
                    "title": officer.get('title'),
                    "age": officer.get('age'),
                    "yearBorn": officer.get('yearBorn'),
                    "totalPay": officer.get('totalPay')
                })
        return officers
    
    def _get_trading_info(self, ticker):
        """Текущая торговая информация"""
        try:
            info = ticker.info
            return {
                "current_price": info.get('currentPrice', info.get('regularMarketPrice')),
                "previous_close": info.get('previousClose'),
                "open": info.get('open', info.get('regularMarketOpen')),
                "day_high": info.get('dayHigh', info.get('regularMarketDayHigh')),
                "day_low": info.get('dayLow', info.get('regularMarketDayLow')),
                "volume": info.get('volume', info.get('regularMarketVolume')),
                "average_volume": info.get('averageVolume'),
                "average_volume_10days": info.get('averageVolume10days'),
                "bid": info.get('bid'),
                "ask": info.get('ask'),
                "bid_size": info.get('bidSize'),
                "ask_size": info.get('askSize'),
                "market_cap": info.get('marketCap'),
                "52_week_high": info.get('fiftyTwoWeekHigh'),
                "52_week_low": info.get('fiftyTwoWeekLow'),
                "50_day_average": info.get('fiftyDayAverage'),
                "200_day_average": info.get('twoHundredDayAverage'),
                "currency": info.get('currency', 'USD'),
                "exchange": info.get('exchange'),
                "quote_type": info.get('quoteType'),
                "exchange_timezone": info.get('exchangeTimezoneName')
            }
        except Exception as e:
            logger.error(f"Error in trading info: {str(e)}")
            return {}
    
    def _get_financial_statements(self, ticker):
        """Финансовые отчеты"""
        try:
            financials = {
                "income_statement": self._convert_df_to_dict(ticker.financials),
                "quarterly_income_statement": self._convert_df_to_dict(ticker.quarterly_financials),
                "balance_sheet": self._convert_df_to_dict(ticker.balance_sheet),
                "quarterly_balance_sheet": self._convert_df_to_dict(ticker.quarterly_balance_sheet),
                "cash_flow": self._convert_df_to_dict(ticker.cashflow),
                "quarterly_cash_flow": self._convert_df_to_dict(ticker.quarterly_cashflow)
            }
            return financials
        except Exception as e:
            logger.error(f"Error in financial statements: {str(e)}")
            return {}
    
    def _get_key_metrics(self, ticker):
        """Ключевые финансовые метрики"""
        try:
            info = ticker.info
            return {
                "valuation_metrics": {
                    "pe_ratio": info.get('trailingPE'),
                    "forward_pe": info.get('forwardPE'),
                    "peg_ratio": info.get('pegRatio'),
                    "price_to_sales": info.get('priceToSalesTrailing12Months'),
                    "price_to_book": info.get('priceToBook'),
                    "enterprise_value": info.get('enterpriseValue'),
                    "enterprise_to_revenue": info.get('enterpriseToRevenue'),
                    "enterprise_to_ebitda": info.get('enterpriseToEbitda')
                },
                "profitability_metrics": {
                    "profit_margin": info.get('profitMargins'),
                    "operating_margin": info.get('operatingMargins'),
                    "return_on_assets": info.get('returnOnAssets'),
                    "return_on_equity": info.get('returnOnEquity'),
                    "revenue_per_share": info.get('revenuePerShare'),
                    "quarterly_revenue_growth": info.get('quarterlyRevenueGrowth'),
                    "gross_profit": info.get('grossProfits'),
                    "ebitda": info.get('ebitda'),
                    "net_income": info.get('netIncomeToCommon'),
                    "earnings_quarterly_growth": info.get('earningsQuarterlyGrowth')
                },
                "financial_health": {
                    "total_cash": info.get('totalCash'),
                    "total_cash_per_share": info.get('totalCashPerShare'),
                    "total_debt": info.get('totalDebt'),
                    "debt_to_equity": info.get('debtToEquity'),
                    "current_ratio": info.get('currentRatio'),
                    "quick_ratio": info.get('quickRatio'),
                    "operating_cash_flow": info.get('operatingCashflow'),
                    "free_cash_flow": info.get('freeCashflow')
                },
                "per_share_data": {
                    "earnings_per_share": info.get('trailingEps'),
                    "forward_eps": info.get('forwardEps'),
                    "book_value_per_share": info.get('bookValue'),
                    "revenue_per_share": info.get('revenuePerShare'),
                    "cash_per_share": info.get('totalCashPerShare')
                }
            }
        except Exception as e:
            logger.error(f"Error in key metrics: {str(e)}")
            return {}
    
    def _get_earnings_data(self, ticker):
        """Данные о прибыли"""
        try:
            earnings_data = {
                "earnings_dates": [],
                "quarterly_earnings": self._convert_df_to_dict(ticker.quarterly_earnings) if hasattr(ticker, 'quarterly_earnings') else {},
                "yearly_earnings": self._convert_df_to_dict(ticker.earnings) if hasattr(ticker, 'earnings') else {}
            }
            
            # Получаем календарь прибыли
            if hasattr(ticker, 'calendar') and ticker.calendar is not None:
                cal = ticker.calendar
                if isinstance(cal, pd.DataFrame) and not cal.empty:
                    earnings_data["next_earnings_date"] = cal.to_dict('records')
                
            return earnings_data
        except Exception as e:
            logger.error(f"Error in earnings data: {str(e)}")
            return {}
    
    def _get_dividends_data(self, ticker):
        """Данные о дивидендах"""
        try:
            info = ticker.info
            dividends = ticker.dividends
            
            dividend_data = {
                "dividend_rate": info.get('dividendRate'),
                "dividend_yield": info.get('dividendYield'),
                "ex_dividend_date": info.get('exDividendDate'),
                "payout_ratio": info.get('payoutRatio'),
                "five_year_avg_dividend_yield": info.get('fiveYearAvgDividendYield'),
                "trailing_annual_dividend_rate": info.get('trailingAnnualDividendRate'),
                "trailing_annual_dividend_yield": info.get('trailingAnnualDividendYield'),
                "dividend_history": []
            }
            
            # История дивидендов
            if not dividends.empty:
                for date, amount in dividends.items():
                    dividend_data["dividend_history"].append({
                        "date": date.strftime('%Y-%m-%d'),
                        "amount": float(amount)
                    })
            
            return dividend_data
        except Exception as e:
            logger.error(f"Error in dividends data: {str(e)}")
            return {}
    
    def _get_analyst_data(self, ticker):
        """Рекомендации аналитиков"""
        try:
            analyst_data = {
                "recommendations": [],
                "price_targets": {},
                "earnings_estimates": {},
                "revenue_estimates": {},
                "eps_trend": {},
                "eps_revisions": {}
            }
            
            # Рекомендации
            if hasattr(ticker, 'recommendations') and ticker.recommendations is not None:
                recs = ticker.recommendations
                if not recs.empty:
                    recent_recs = recs.tail(10)  # Последние 10 рекомендаций
                    for idx, row in recent_recs.iterrows():
                        analyst_data["recommendations"].append({
                            "date": idx.strftime('%Y-%m-%d'),
                            "firm": row.get('Firm', ''),
                            "to_grade": row.get('To Grade', ''),
                            "from_grade": row.get('From Grade', ''),
                            "action": row.get('Action', '')
                        })
            
            # Целевые цены
            info = ticker.info
            analyst_data["price_targets"] = {
                "current": info.get('currentPrice'),
                "target_high": info.get('targetHighPrice'),
                "target_low": info.get('targetLowPrice'),
                "target_mean": info.get('targetMeanPrice'),
                "target_median": info.get('targetMedianPrice'),
                "number_of_analysts": info.get('numberOfAnalystOpinions')
            }
            
            # Оценки прибыли
            if hasattr(ticker, 'earnings_estimate'):
                analyst_data["earnings_estimates"] = self._convert_df_to_dict(ticker.earnings_estimate)
            
            # Оценки выручки
            if hasattr(ticker, 'revenue_estimate'):
                analyst_data["revenue_estimates"] = self._convert_df_to_dict(ticker.revenue_estimate)
            
            return analyst_data
        except Exception as e:
            logger.error(f"Error in analyst data: {str(e)}")
            return {}
    
    def _get_institutional_data(self, ticker):
        """Данные об институциональных держателях"""
        try:
            institutional_data = {
                "major_holders": {},
                "institutional_holders": [],
                "mutualfund_holders": []
            }
            
            # Основные держатели
            if hasattr(ticker, 'major_holders') and ticker.major_holders is not None:
                mh = ticker.major_holders
                if not mh.empty:
                    for idx, row in mh.iterrows():
                        institutional_data["major_holders"][row[1]] = row[0]
            
            # Институциональные держатели
            if hasattr(ticker, 'institutional_holders') and ticker.institutional_holders is not None:
                ih = ticker.institutional_holders
                if not ih.empty:
                    for idx, row in ih.iterrows():
                        institutional_data["institutional_holders"].append({
                            "holder": row.get('Holder', ''),
                            "shares": row.get('Shares', 0),
                            "date_reported": row.get('Date Reported', ''),
                            "percent_out": row.get('% Out', 0),
                            "value": row.get('Value', 0)
                        })
            
            # Держатели взаимных фондов
            if hasattr(ticker, 'mutualfund_holders') and ticker.mutualfund_holders is not None:
                mfh = ticker.mutualfund_holders
                if not mfh.empty:
                    for idx, row in mfh.iterrows():
                        institutional_data["mutualfund_holders"].append({
                            "holder": row.get('Holder', ''),
                            "shares": row.get('Shares', 0),
                            "date_reported": row.get('Date Reported', ''),
                            "percent_out": row.get('% Out', 0),
                            "value": row.get('Value', 0)
                        })
            
            return institutional_data
        except Exception as e:
            logger.error(f"Error in institutional data: {str(e)}")
            return {}
    
    def _get_historical_prices(self, ticker, period='1y'):
        """Исторические цены"""
        try:
            hist = ticker.history(period=period)
            historical_data = []
            
            if not hist.empty:
                for index, row in hist.iterrows():
                    historical_data.append({
                        "date": index.strftime('%Y-%m-%d'),
                        "open": round(row['Open'], 2),
                        "high": round(row['High'], 2),
                        "low": round(row['Low'], 2),
                        "close": round(row['Close'], 2),
                        "volume": int(row['Volume']),
                        "dividends": float(row.get('Dividends', 0)),
                        "stock_splits": float(row.get('Stock Splits', 0))
                    })
            
            return historical_data
        except Exception as e:
            logger.error(f"Error in historical prices: {str(e)}")
            return []
    
    def _get_options_data(self, ticker):
        """Данные об опционах"""
        try:
            options_data = {
                "expiration_dates": [],
                "options_chain": {}
            }
            
            # Получаем даты экспирации
            if hasattr(ticker, 'options'):
                options_data["expiration_dates"] = list(ticker.options)
                
                # Получаем цепочку опционов для ближайшей даты
                if options_data["expiration_dates"]:
                    nearest_date = options_data["expiration_dates"][0]
                    opt = ticker.option_chain(nearest_date)
                    
                    # Calls
                    if hasattr(opt, 'calls') and not opt.calls.empty:
                        options_data["options_chain"]["calls"] = opt.calls.head(10).to_dict('records')
                    
                    # Puts
                    if hasattr(opt, 'puts') and not opt.puts.empty:
                        options_data["options_chain"]["puts"] = opt.puts.head(10).to_dict('records')
            
            return options_data
        except Exception as e:
            logger.error(f"Error in options data: {str(e)}")
            return {}
    
    def _get_recent_news(self, ticker):
        """Последние новости"""
        try:
            news_data = []
            
            if hasattr(ticker, 'news'):
                for item in ticker.news[:5]:  # Последние 5 новостей
                    news_data.append({
                        "title": item.get('title'),
                        "publisher": item.get('publisher'),
                        "link": item.get('link'),
                        "published_time": datetime.fromtimestamp(
                            item.get('providerPublishTime', 0)
                        ).isoformat() if item.get('providerPublishTime') else None,
                        "type": item.get('type'),
                        "thumbnail": item.get('thumbnail', {}).get('resolutions', [{}])[0].get('url') if item.get('thumbnail') else None
                    })
            
            return news_data
        except Exception as e:
            logger.error(f"Error in news data: {str(e)}")
            return []
    
    def _convert_df_to_dict(self, df):
        """Конвертировать DataFrame в словарь для JSON"""
        if df is None or df.empty:
            return {}
        
        try:
            # Конвертируем индекс в строку для JSON совместимости
            result = {}
            for col in df.columns:
                result[col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else str(col)] = {}
                for idx in df.index:
                    value = df.loc[idx, col]
                    # Обрабатываем NaN значения
                    if pd.isna(value):
                        value = None
                    elif isinstance(value, (int, float)):
                        value = float(value)
                    result[col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else str(col)][str(idx)] = value
            return result
        except Exception as e:
            logger.error(f"Error converting dataframe: {str(e)}")
            return {}
    
    def get_financial_summary(self, symbol):
        """Получить краткую финансовую сводку"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "success": True,
                "symbol": symbol,
                "summary": {
                    "company": info.get('longName'),
                    "price": info.get('currentPrice'),
                    "market_cap": info.get('marketCap'),
                    "pe_ratio": info.get('trailingPE'),
                    "earnings_per_share": info.get('trailingEps'),
                    "dividend_yield": info.get('dividendYield'),
                    "52_week_range": f"{info.get('fiftyTwoWeekLow')} - {info.get('fiftyTwoWeekHigh')}",
                    "revenue": info.get('totalRevenue'),
                    "profit_margin": info.get('profitMargins'),
                    "recommendation": info.get('recommendationKey')
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting summary for {symbol}: {str(e)}")
            return {"success": False, "error": str(e)}