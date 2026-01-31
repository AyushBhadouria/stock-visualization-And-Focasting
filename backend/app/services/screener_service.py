"""
Stock screener service for filtering stocks by various criteria
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import yfinance as yf


class ScreenerService:
    """Stock screening based on multiple criteria"""
    
    @staticmethod
    def get_stock_info(symbol: str) -> Dict[str, Any]:
        """Get comprehensive stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "symbol": symbol,
                "name": info.get("longName", ""),
                "price": info.get("currentPrice", 0),
                "marketCap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", None),
                "volume": info.get("volume", 0),
                "avgVolume": info.get("averageVolume", 0),
                "52WeekHigh": info.get("fiftyTwoWeekHigh", 0),
                "52WeekLow": info.get("fiftyTwoWeekLow", 0),
                "dividend_yield": info.get("dividendYield", 0),
                "beta": info.get("beta", 0),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", "")
            }
        except Exception as e:
            print(f"Error fetching stock info for {symbol}: {e}")
            return {}
    
    @staticmethod
    def calculate_rsi(symbol: str, period: int = 14) -> float:
        """Calculate RSI for a stock"""
        try:
            data = yf.download(symbol, period="3mo", interval="1d", progress=False)
            if data.empty:
                return None
            
            closes = data["Close"]
            delta = closes.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return float(rsi.iloc[-1])
        except:
            return None
    
    @staticmethod
    def calculate_sma_50_200(symbol: str) -> Dict[str, float]:
        """Calculate 50 and 200 day SMAs"""
        try:
            data = yf.download(symbol, period="1y", interval="1d", progress=False)
            if data.empty:
                return {}
            
            sma_50 = data["Close"].rolling(window=50).mean().iloc[-1]
            sma_200 = data["Close"].rolling(window=200).mean().iloc[-1]
            
            return {
                "sma_50": float(sma_50),
                "sma_200": float(sma_200),
                "crossover": "bullish" if sma_50 > sma_200 else "bearish"
            }
        except:
            return {}
    
    @staticmethod
    def screen_by_criteria(symbols: List[str], criteria: Dict[str, Any]) -> List[Dict]:
        """
        Screen stocks based on multiple criteria
        
        criteria can include:
        {
            "price_min": 10,
            "price_max": 500,
            "market_cap_min": 1000000000,
            "market_cap_max": 999999999999,
            "pe_ratio_max": 25,
            "rsi_oversold": True,  # RSI < 30
            "rsi_overbought": True,  # RSI > 70
            "sma_crossover": "bullish",  # or "bearish"
            "min_volume": 1000000
        }
        """
        results = []
        
        for symbol in symbols:
            try:
                stock_info = ScreenerService.get_stock_info(symbol)
                if not stock_info:
                    continue
                
                # Check price range
                if criteria.get("price_min"):
                    if stock_info.get("price", 0) < criteria["price_min"]:
                        continue
                if criteria.get("price_max"):
                    if stock_info.get("price", 0) > criteria["price_max"]:
                        continue
                
                # Check market cap
                if criteria.get("market_cap_min"):
                    if stock_info.get("marketCap", 0) < criteria["market_cap_min"]:
                        continue
                if criteria.get("market_cap_max"):
                    if stock_info.get("marketCap", 0) > criteria["market_cap_max"]:
                        continue
                
                # Check P/E ratio
                if criteria.get("pe_ratio_max"):
                    pe = stock_info.get("pe_ratio")
                    if pe and pe > criteria["pe_ratio_max"]:
                        continue
                
                # Check volume
                if criteria.get("min_volume"):
                    if stock_info.get("volume", 0) < criteria["min_volume"]:
                        continue
                
                # Check RSI
                rsi = ScreenerService.calculate_rsi(symbol)
                if rsi:
                    if criteria.get("rsi_oversold") and rsi >= 30:
                        continue
                    if criteria.get("rsi_overbought") and rsi <= 70:
                        continue
                
                # Check SMA crossover
                if criteria.get("sma_crossover"):
                    sma_data = ScreenerService.calculate_sma_50_200(symbol)
                    if sma_data and sma_data.get("crossover") != criteria["sma_crossover"]:
                        continue
                
                stock_info["rsi"] = rsi
                stock_info.update(ScreenerService.calculate_sma_50_200(symbol))
                results.append(stock_info)
            
            except Exception as e:
                print(f"Error screening {symbol}: {e}")
                continue
        
        return results
    
    @staticmethod
    def get_top_gainers(limit: int = 10) -> List[Dict]:
        """Get top gaining stocks (requires real-time data source)"""
        # This would typically require a financial data API
        # For now, return empty - to be implemented with real data source
        return []
    
    @staticmethod
    def get_top_losers(limit: int = 10) -> List[Dict]:
        """Get top losing stocks"""
        # This would typically require a financial data API
        return []
    
    @staticmethod
    def get_most_active(limit: int = 10) -> List[Dict]:
        """Get most active stocks by volume"""
        # This would typically require a financial data API
        return []
