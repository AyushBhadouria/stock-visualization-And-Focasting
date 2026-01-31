"""
Advanced charting service with multiple chart types and drawing tools
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import yfinance as yf


class ChartingService:
    """Handles advanced charting capabilities"""
    
    @staticmethod
    def get_ohlc_data(symbol: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
        """
        Get OHLC (Open, High, Low, Close) data for charting
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo)
        """
        try:
            data = yf.download(symbol, period=period, interval=interval, progress=False)
            if data.empty:
                return pd.DataFrame()
            
            # Reset index to convert datetime index to column
            data = data.reset_index()
            
            # Handle column naming - yfinance may use 'Date' or 'Datetime'
            if 'Datetime' in data.columns:
                data.rename(columns={'Datetime': 'Date'}, inplace=True)
            
            # Add volume if not present
            if "Volume" not in data.columns:
                data["Volume"] = 0
                
            return data
        except Exception as e:
            print(f"Error fetching OHLC data for {symbol}: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def get_candlestick_data(symbol: str, period: str = "1mo") -> List[Dict]:
        """Format data for candlestick chart"""
        df = ChartingService.get_ohlc_data(symbol, period, "1d")
        if df.empty:
            return []
        
        candlesticks = []
        for idx, row in df.iterrows():
            try:
                # Handle both Date and Datetime column names
                date_col = 'Date' if 'Date' in row.index else 'Datetime'
                date_val = row[date_col]
                
                # Convert to timestamp
                if hasattr(date_val, 'timestamp'):
                    timestamp = int(date_val.timestamp())
                else:
                    timestamp = int(pd.Timestamp(date_val).timestamp())
                
                candlesticks.append({
                    "time": timestamp,
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": float(row.get("Volume", 0))
                })
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                continue
        
        return candlesticks
    
    @staticmethod
    def get_heikin_ashi(symbol: str, period: str = "1mo") -> List[Dict]:
        """Calculate Heikin Ashi candlesticks"""
        df = ChartingService.get_ohlc_data(symbol, period, "1d")
        if df.empty:
            return []
        
        df = df.copy()
        df["HA_Close"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4
        
        df["HA_Open"] = 0.0
        df.loc[0, "HA_Open"] = (df.loc[0, "Open"] + df.loc[0, "Close"]) / 2
        
        for i in range(1, len(df)):
            df.loc[i, "HA_Open"] = (df.loc[i-1, "HA_Open"] + df.loc[i-1, "HA_Close"]) / 2
        
        df["HA_High"] = df[["HA_Open", "HA_Close", "High"]].max(axis=1)
        df["HA_Low"] = df[["HA_Open", "HA_Close", "Low"]].min(axis=1)
        
        ha_candles = []
        for _, row in df.iterrows():
            ha_candles.append({
                "time": int(pd.Timestamp(row["Date"]).timestamp()),
                "open": float(row["HA_Open"]),
                "high": float(row["HA_High"]),
                "low": float(row["HA_Low"]),
                "close": float(row["HA_Close"]),
                "volume": float(row.get("Volume", 0))
            })
        return ha_candles
    
    @staticmethod
    def compare_stocks(symbols: List[str], period: str = "1mo") -> Dict[str, List[Dict]]:
        """Get data for comparing multiple stocks"""
        comparison = {}
        for symbol in symbols:
            df = ChartingService.get_ohlc_data(symbol, period, "1d")
            if not df.empty:
                # Normalize to percentage change from first close
                first_close = df.iloc[0]["Close"]
                df["PctChange"] = ((df["Close"] - first_close) / first_close * 100)
                
                comparison[symbol] = [
                    {
                        "time": int(pd.Timestamp(row["Date"]).timestamp()),
                        "close": float(row["Close"]),
                        "pctChange": float(row["PctChange"])
                    }
                    for _, row in df.iterrows()
                ]
        return comparison
    
    @staticmethod
    def get_fibonacci_levels(symbol: str, period: str = "1mo") -> Dict[str, float]:
        """Calculate Fibonacci retracement levels"""
        df = ChartingService.get_ohlc_data(symbol, period, "1d")
        if df.empty:
            return {}
        
        high = df["High"].max()
        low = df["Low"].min()
        diff = high - low
        
        levels = {
            "0%": low,
            "23.6%": low + (diff * 0.236),
            "38.2%": low + (diff * 0.382),
            "50%": low + (diff * 0.5),
            "61.8%": low + (diff * 0.618),
            "78.6%": low + (diff * 0.786),
            "100%": high
        }
        
        return {k: float(v) for k, v in levels.items()}
    
    @staticmethod
    def get_pivot_points(symbol: str, period: str = "1d") -> Dict[str, float]:
        """Calculate daily pivot points"""
        df = ChartingService.get_ohlc_data(symbol, period, "1d")
        if df.empty:
            return {}
        
        last = df.iloc[-1]
        high, low, close = last["High"], last["Low"], last["Close"]
        
        pivot = (high + low + close) / 3
        
        return {
            "resistance3": pivot + (high - low) * 1.5,
            "resistance2": pivot + (high - low) * 1.0,
            "resistance1": pivot + (high - low) * 0.5,
            "pivot": float(pivot),
            "support1": pivot - (high - low) * 0.5,
            "support2": pivot - (high - low) * 1.0,
            "support3": pivot - (high - low) * 1.5,
        }
    
    @staticmethod
    def get_support_resistance(symbol: str, period: str = "1mo", num_levels: int = 3) -> Dict[str, List[float]]:
        """Identify support and resistance levels"""
        df = ChartingService.get_ohlc_data(symbol, period, "1d")
        if df.empty:
            return {"support": [], "resistance": []}
        
        # Simple approach: find local minima (support) and maxima (resistance)
        highs = df["High"].values
        lows = df["Low"].values
        
        # Find support levels (local minima)
        support = []
        for i in range(1, len(lows) - 1):
            if lows[i] < lows[i-1] and lows[i] < lows[i+1]:
                support.append(float(lows[i]))
        
        # Find resistance levels (local maxima)
        resistance = []
        for i in range(1, len(highs) - 1):
            if highs[i] > highs[i-1] and highs[i] > highs[i+1]:
                resistance.append(float(highs[i]))
        
        # Sort and get top N
        support = sorted(set(support), reverse=True)[:num_levels]
        resistance = sorted(set(resistance), reverse=True)[:num_levels]
        
        return {
            "support": support,
            "resistance": resistance
        }
    
    @staticmethod
    def calculate_channels(symbol: str, period: str = "1mo", window: int = 20) -> Dict[str, List]:
        """Calculate Donchian Channels"""
        df = ChartingService.get_ohlc_data(symbol, period, "1d")
        if df.empty:
            return {"upper": [], "lower": [], "middle": []}
        
        df["HighestHigh"] = df["High"].rolling(window=window).max()
        df["LowestLow"] = df["Low"].rolling(window=window).min()
        df["MiddleBand"] = (df["HighestHigh"] + df["LowestLow"]) / 2
        
        return {
            "upper": df["HighestHigh"].dropna().tolist(),
            "lower": df["LowestLow"].dropna().tolist(),
            "middle": df["MiddleBand"].dropna().tolist()
        }
