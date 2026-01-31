"""
Advanced technical indicators service
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import yfinance as yf


class AdvancedIndicatorsService:
    """Advanced technical indicators beyond basic moving averages"""
    
    @staticmethod
    def get_ohlc(symbol: str, period: str = "1mo") -> pd.DataFrame:
        """Get OHLC data"""
        try:
            data = yf.download(symbol, period=period, interval="1d", progress=False)
            return data.reset_index() if not data.empty else pd.DataFrame()
        except:
            return pd.DataFrame()
    
    @staticmethod
    def calculate_atr(symbol: str, period: int = 14) -> Dict[str, List]:
        """Average True Range - measures volatility"""
        df = AdvancedIndicatorsService.get_ohlc(symbol)
        if df.empty:
            return {}
        
        df["TR"] = np.maximum(
            df["High"] - df["Low"],
            np.maximum(
                abs(df["High"] - df["Close"].shift()),
                abs(df["Low"] - df["Close"].shift())
            )
        )
        
        df["ATR"] = df["TR"].rolling(window=period).mean()
        
        return {
            "values": df["ATR"].dropna().tolist(),
            "dates": df["Date"].dropna().tolist()
        }
    
    @staticmethod
    def calculate_adx(symbol: str, period: int = 14) -> Dict[str, List]:
        """Average Directional Index - measures trend strength"""
        df = AdvancedIndicatorsService.get_ohlc(symbol)
        if df.empty:
            return {}
        
        df["HighDiff"] = df["High"].diff()
        df["LowDiff"] = -df["Low"].diff()
        
        df["PlusDM"] = np.where((df["HighDiff"] > df["LowDiff"]) & (df["HighDiff"] > 0), 
                               df["HighDiff"], 0)
        df["MinusDM"] = np.where((df["LowDiff"] > df["HighDiff"]) & (df["LowDiff"] > 0), 
                                df["LowDiff"], 0)
        
        tr = np.maximum(
            df["High"] - df["Low"],
            np.maximum(
                abs(df["High"] - df["Close"].shift()),
                abs(df["Low"] - df["Close"].shift())
            )
        )
        
        df["TR"] = tr
        df["ATR"] = df["TR"].rolling(window=period).mean()
        
        df["PlusDI"] = 100 * (df["PlusDM"].rolling(window=period).mean() / df["ATR"])
        df["MinusDI"] = 100 * (df["MinusDM"].rolling(window=period).mean() / df["ATR"])
        
        df["DX"] = 100 * abs(df["PlusDI"] - df["MinusDI"]) / (df["PlusDI"] + df["MinusDI"])
        df["ADX"] = df["DX"].rolling(window=period).mean()
        
        return {
            "adx": df["ADX"].dropna().tolist(),
            "plusDI": df["PlusDI"].dropna().tolist(),
            "minusDI": df["MinusDI"].dropna().tolist(),
            "dates": df["Date"].dropna().tolist()
        }
    
    @staticmethod
    def calculate_ichimoku(symbol: str) -> Dict[str, List]:
        """Ichimoku Cloud indicator"""
        df = AdvancedIndicatorsService.get_ohlc(symbol)
        if df.empty:
            return {}
        
        # Tenkan-sen (Conversion Line)
        high_9 = df["High"].rolling(window=9).max()
        low_9 = df["Low"].rolling(window=9).min()
        df["tenkan"] = (high_9 + low_9) / 2
        
        # Kijun-sen (Base Line)
        high_26 = df["High"].rolling(window=26).max()
        low_26 = df["Low"].rolling(window=26).min()
        df["kijun"] = (high_26 + low_26) / 2
        
        # Senkou Span A (Leading Span A)
        df["senkou_a"] = ((df["tenkan"] + df["kijun"]) / 2).shift(26)
        
        # Senkou Span B (Leading Span B)
        high_52 = df["High"].rolling(window=52).max()
        low_52 = df["Low"].rolling(window=52).min()
        df["senkou_b"] = ((high_52 + low_52) / 2).shift(26)
        
        # Chikou Span (Lagging Span)
        df["chikou"] = df["Close"].shift(-26)
        
        return {
            "tenkan": df["tenkan"].dropna().tolist(),
            "kijun": df["kijun"].dropna().tolist(),
            "senkou_a": df["senkou_a"].dropna().tolist(),
            "senkou_b": df["senkou_b"].dropna().tolist(),
            "chikou": df["chikou"].dropna().tolist(),
            "dates": df["Date"].dropna().tolist()
        }
    
    @staticmethod
    def calculate_obv(symbol: str) -> Dict[str, List]:
        """On Balance Volume"""
        df = AdvancedIndicatorsService.get_ohlc(symbol)
        if df.empty:
            return {}
        
        if "Volume" not in df.columns:
            return {}
        
        df["OBV"] = 0.0
        df.loc[0, "OBV"] = df.loc[0, "Volume"]
        
        for i in range(1, len(df)):
            if df.loc[i, "Close"] > df.loc[i-1, "Close"]:
                df.loc[i, "OBV"] = df.loc[i-1, "OBV"] + df.loc[i, "Volume"]
            elif df.loc[i, "Close"] < df.loc[i-1, "Close"]:
                df.loc[i, "OBV"] = df.loc[i-1, "OBV"] - df.loc[i, "Volume"]
            else:
                df.loc[i, "OBV"] = df.loc[i-1, "OBV"]
        
        return {
            "values": df["OBV"].tolist(),
            "dates": df["Date"].tolist()
        }
    
    @staticmethod
    def calculate_vwap(symbol: str) -> Dict[str, List]:
        """Volume Weighted Average Price"""
        df = AdvancedIndicatorsService.get_ohlc(symbol)
        if df.empty:
            return {}
        
        if "Volume" not in df.columns:
            return {}
        
        df["TP"] = (df["High"] + df["Low"] + df["Close"]) / 3
        df["VWAP"] = (df["TP"] * df["Volume"]).rolling(window=20).sum() / df["Volume"].rolling(window=20).sum()
        
        return {
            "values": df["VWAP"].dropna().tolist(),
            "dates": df["Date"].dropna().tolist()
        }
    
    @staticmethod
    def calculate_macd(symbol: str, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, List]:
        """MACD - Moving Average Convergence Divergence"""
        df = AdvancedIndicatorsService.get_ohlc(symbol)
        if df.empty:
            return {}
        
        df["EMA_fast"] = df["Close"].ewm(span=fast).mean()
        df["EMA_slow"] = df["Close"].ewm(span=slow).mean()
        df["MACD"] = df["EMA_fast"] - df["EMA_slow"]
        df["Signal"] = df["MACD"].ewm(span=signal).mean()
        df["Histogram"] = df["MACD"] - df["Signal"]
        
        return {
            "macd": df["MACD"].dropna().tolist(),
            "signal": df["Signal"].dropna().tolist(),
            "histogram": df["Histogram"].dropna().tolist(),
            "dates": df["Date"].dropna().tolist()
        }
    
    @staticmethod
    def calculate_stochastic(symbol: str, period: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> Dict[str, List]:
        """Stochastic Oscillator"""
        df = AdvancedIndicatorsService.get_ohlc(symbol)
        if df.empty:
            return {}
        
        lowest_low = df["Low"].rolling(window=period).min()
        highest_high = df["High"].rolling(window=period).max()
        
        df["K"] = ((df["Close"] - lowest_low) / (highest_high - lowest_low)) * 100
        df["K_smooth"] = df["K"].rolling(window=smooth_k).mean()
        df["D"] = df["K_smooth"].rolling(window=smooth_d).mean()
        
        return {
            "k": df["K"].dropna().tolist(),
            "d": df["D"].dropna().tolist(),
            "dates": df["Date"].dropna().tolist()
        }
    
    @staticmethod
    def calculate_bollinger_bands(symbol: str, period: int = 20, std_dev: float = 2) -> Dict[str, List]:
        """Bollinger Bands"""
        df = AdvancedIndicatorsService.get_ohlc(symbol)
        if df.empty:
            return {}
        
        df["SMA"] = df["Close"].rolling(window=period).mean()
        df["StdDev"] = df["Close"].rolling(window=period).std()
        df["Upper"] = df["SMA"] + (df["StdDev"] * std_dev)
        df["Lower"] = df["SMA"] - (df["StdDev"] * std_dev)
        
        return {
            "upper": df["Upper"].dropna().tolist(),
            "middle": df["SMA"].dropna().tolist(),
            "lower": df["Lower"].dropna().tolist(),
            "dates": df["Date"].dropna().tolist()
        }
