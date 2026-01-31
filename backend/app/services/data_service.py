import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
import os
from datetime import datetime, timedelta

class DataService:
    def __init__(self):
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_KEY")
        self.polygon_key = os.getenv("POLYGON_KEY")
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> Dict:
        """Fetch stock data using yfinance"""
        try:
            print(f"Fetching data for {symbol} with period {period}")
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist = ticker.history(period=period)
            if hist.empty:
                print(f"No historical data found for {symbol}")
                return {"error": f"No data found for {symbol}"}
            
            # Get stock info
            try:
                info = ticker.info
            except:
                info = {}
            
            # Convert history to records
            hist_reset = hist.reset_index()
            history_records = []
            
            for _, row in hist_reset.iterrows():
                history_records.append({
                    "Date": row['Date'].strftime('%Y-%m-%d') if hasattr(row['Date'], 'strftime') else str(row['Date']),
                    "Open": float(row['Open']),
                    "High": float(row['High']),
                    "Low": float(row['Low']),
                    "Close": float(row['Close']),
                    "Volume": int(row['Volume'])
                })
            
            current_price = float(hist['Close'].iloc[-1])
            prev_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
            change = current_price - prev_price
            change_percent = (change / prev_price) * 100 if prev_price != 0 else 0
            
            result = {
                "symbol": symbol,
                "name": info.get("longName", f"{symbol} Inc."),
                "price": current_price,
                "change": change,
                "change_percent": change_percent,
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "history": history_records
            }
            
            print(f"Successfully fetched {len(history_records)} records for {symbol}")
            return result
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return {"error": str(e)}
    
    def search_stocks(self, query: str) -> List[Dict]:
        """Search for stocks by symbol"""
        try:
            # Common stock symbols for testing
            common_stocks = {
                "AAPL": "Apple Inc.",
                "GOOGL": "Alphabet Inc.",
                "MSFT": "Microsoft Corporation",
                "TSLA": "Tesla Inc.",
                "AMZN": "Amazon.com Inc.",
                "META": "Meta Platforms Inc.",
                "NVDA": "NVIDIA Corporation",
                "NFLX": "Netflix Inc."
            }
            
            results = []
            query_upper = query.upper()
            
            # Check if query matches any common stocks
            for symbol, name in common_stocks.items():
                if query_upper in symbol or query_upper in name.upper():
                    try:
                        ticker = yf.Ticker(symbol)
                        info = ticker.info
                        results.append({
                            "symbol": symbol,
                            "name": name,
                            "exchange": info.get("exchange", "NASDAQ"),
                            "price": info.get("currentPrice", 0)
                        })
                    except:
                        results.append({
                            "symbol": symbol,
                            "name": name,
                            "exchange": "NASDAQ",
                            "price": 0
                        })
            
            # Also try the query as a direct symbol
            if query_upper not in [r["symbol"] for r in results]:
                try:
                    ticker = yf.Ticker(query_upper)
                    info = ticker.info
                    if info.get("longName"):
                        results.append({
                            "symbol": query_upper,
                            "name": info.get("longName"),
                            "exchange": info.get("exchange", "NASDAQ"),
                            "price": info.get("currentPrice", 0)
                        })
                except:
                    pass
            
            return results[:5]  # Limit to 5 results
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def get_real_time_quote(self, symbol: str) -> Dict:
        """Get real-time quote"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            
            if hist.empty:
                return {"error": f"No data found for {symbol}"}
            
            current_price = float(hist['Close'].iloc[-1])
            
            try:
                info = ticker.info
                change = info.get("regularMarketChange", 0)
                change_percent = info.get("regularMarketChangePercent", 0)
                volume = info.get("regularMarketVolume", int(hist['Volume'].iloc[-1]))
            except:
                # Fallback calculation
                prev_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                change = current_price - prev_price
                change_percent = (change / prev_price) * 100 if prev_price != 0 else 0
                volume = int(hist['Volume'].iloc[-1])
            
            return {
                "symbol": symbol,
                "price": current_price,
                "change": change,
                "change_percent": change_percent,
                "volume": volume,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Quote error for {symbol}: {str(e)}")
            return {"error": str(e)}