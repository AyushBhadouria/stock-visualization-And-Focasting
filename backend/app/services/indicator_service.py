import pandas as pd
import numpy as np
from typing import Dict, List

class IndicatorService:
    
    def calculate_sma(self, prices: List[float], period: int = 20) -> List[float]:
        """Simple Moving Average"""
        try:
            df = pd.Series(prices)
            sma = df.rolling(window=period).mean()
            return sma.fillna(method='bfill').tolist()
        except:
            return [0] * len(prices)
    
    def calculate_ema(self, prices: List[float], period: int = 20) -> List[float]:
        """Exponential Moving Average"""
        try:
            df = pd.Series(prices)
            ema = df.ewm(span=period).mean()
            return ema.fillna(method='bfill').tolist()
        except:
            return [0] * len(prices)
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> List[float]:
        """Relative Strength Index"""
        try:
            df = pd.Series(prices)
            delta = df.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.fillna(50).tolist()
        except:
            return [50] * len(prices)
    
    def calculate_macd(self, prices: List[float]) -> Dict:
        """MACD Indicator"""
        try:
            df = pd.Series(prices)
            ema12 = df.ewm(span=12).mean()
            ema26 = df.ewm(span=26).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9).mean()
            histogram = macd - signal
            
            return {
                "macd": macd.fillna(0).tolist(),
                "signal": signal.fillna(0).tolist(),
                "histogram": histogram.fillna(0).tolist()
            }
        except:
            return {
                "macd": [0] * len(prices),
                "signal": [0] * len(prices),
                "histogram": [0] * len(prices)
            }
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20) -> Dict:
        """Bollinger Bands"""
        try:
            df = pd.Series(prices)
            sma = df.rolling(window=period).mean()
            std = df.rolling(window=period).std()
            
            return {
                "upper": (sma + (std * 2)).fillna(method='bfill').tolist(),
                "middle": sma.fillna(method='bfill').tolist(),
                "lower": (sma - (std * 2)).fillna(method='bfill').tolist()
            }
        except:
            return {
                "upper": prices,
                "middle": prices,
                "lower": prices
            }
    
    def calculate_stochastic(self, high: List[float], low: List[float], close: List[float]) -> Dict:
        """Stochastic Oscillator"""
        try:
            high_df = pd.Series(high)
            low_df = pd.Series(low)
            close_df = pd.Series(close)
            
            lowest_low = low_df.rolling(window=14).min()
            highest_high = high_df.rolling(window=14).max()
            
            k_percent = 100 * ((close_df - lowest_low) / (highest_high - lowest_low))
            d_percent = k_percent.rolling(window=3).mean()
            
            return {
                "k": k_percent.fillna(50).tolist(),
                "d": d_percent.fillna(50).tolist()
            }
        except:
            return {
                "k": [50] * len(close),
                "d": [50] * len(close)
            }
    
    def calculate_all_indicators(self, ohlcv_data: List[Dict]) -> Dict:
        """Calculate all indicators for OHLCV data"""
        try:
            df = pd.DataFrame(ohlcv_data)
            
            close_prices = df['Close'].tolist()
            high_prices = df['High'].tolist()
            low_prices = df['Low'].tolist()
            
            return {
                "sma_20": self.calculate_sma(close_prices, 20),
                "sma_50": self.calculate_sma(close_prices, 50),
                "ema_12": self.calculate_ema(close_prices, 12),
                "ema_26": self.calculate_ema(close_prices, 26),
                "rsi": self.calculate_rsi(close_prices),
                "macd": self.calculate_macd(close_prices),
                "bollinger": self.calculate_bollinger_bands(close_prices),
                "stochastic": self.calculate_stochastic(high_prices, low_prices, close_prices)
            }
        except Exception as e:
            print(f"Indicator calculation error: {str(e)}")
            return {}