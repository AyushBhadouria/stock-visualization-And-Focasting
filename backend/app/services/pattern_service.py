import pandas as pd
import numpy as np
from typing import Dict, List

class PatternService:
    
    def detect_candlestick_patterns(self, ohlc_data: List[Dict]) -> Dict:
        """Detect basic candlestick patterns"""
        df = pd.DataFrame(ohlc_data)
        
        patterns = {}
        
        # Simple Doji detection
        body_size = abs(df['Close'] - df['Open'])
        candle_range = df['High'] - df['Low']
        doji_threshold = candle_range * 0.1
        
        patterns['doji'] = (body_size <= doji_threshold).astype(int).tolist()
        
        # Simple Hammer detection
        lower_shadow = df[['Open', 'Close']].min(axis=1) - df['Low']
        upper_shadow = df['High'] - df[['Open', 'Close']].max(axis=1)
        
        hammer_condition = (lower_shadow >= 2 * body_size) & (upper_shadow <= body_size)
        patterns['hammer'] = hammer_condition.astype(int).tolist()
        
        return patterns
    
    def detect_support_resistance(self, prices: List[float], window: int = 20) -> Dict:
        """Detect support and resistance levels"""
        prices_array = np.array(prices)
        
        # Find local minima (support) and maxima (resistance)
        support_levels = []
        resistance_levels = []
        
        for i in range(window, len(prices_array) - window):
            # Support: local minimum
            if prices_array[i] == min(prices_array[i-window:i+window+1]):
                support_levels.append({
                    'level': prices_array[i],
                    'index': i,
                    'strength': self._calculate_level_strength(prices_array, i, prices_array[i])
                })
            
            # Resistance: local maximum
            if prices_array[i] == max(prices_array[i-window:i+window+1]):
                resistance_levels.append({
                    'level': prices_array[i],
                    'index': i,
                    'strength': self._calculate_level_strength(prices_array, i, prices_array[i])
                })
        
        return {
            'support': support_levels[-5:],  # Last 5 support levels
            'resistance': resistance_levels[-5:]  # Last 5 resistance levels
        }
    
    def _calculate_level_strength(self, prices: np.array, index: int, level: float, tolerance: float = 0.02) -> int:
        """Calculate strength of support/resistance level"""
        touches = 0
        for price in prices:
            if abs(price - level) / level <= tolerance:
                touches += 1
        return touches
    
    def detect_trend_lines(self, prices: List[float], dates: List[str]) -> Dict:
        """Detect trend lines"""
        prices_array = np.array(prices)
        
        # Simple trend line detection using linear regression on peaks/troughs
        peaks = []
        troughs = []
        
        for i in range(2, len(prices_array) - 2):
            # Peak
            if prices_array[i] > prices_array[i-1] and prices_array[i] > prices_array[i+1]:
                peaks.append((i, prices_array[i]))
            
            # Trough
            if prices_array[i] < prices_array[i-1] and prices_array[i] < prices_array[i+1]:
                troughs.append((i, prices_array[i]))
        
        trend_lines = {
            'uptrend': self._fit_trend_line(troughs[-4:]) if len(troughs) >= 4 else None,
            'downtrend': self._fit_trend_line(peaks[-4:]) if len(peaks) >= 4 else None
        }
        
        return trend_lines
    
    def _fit_trend_line(self, points: List[tuple]) -> Dict:
        """Fit trend line through points"""
        if len(points) < 2:
            return None
        
        x = np.array([p[0] for p in points])
        y = np.array([p[1] for p in points])
        
        # Linear regression
        slope, intercept = np.polyfit(x, y, 1)
        
        return {
            'slope': float(slope),
            'intercept': float(intercept),
            'points': points
        }