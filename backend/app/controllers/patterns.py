from fastapi import APIRouter, Depends, HTTPException
from app.services.pattern_service import PatternService
from app.services.data_service import DataService

router = APIRouter()
pattern_service = PatternService()
data_service = DataService()

@router.get("/{symbol}/candlestick")
async def get_candlestick_patterns(symbol: str, period: str = "3mo"):
    """Get candlestick patterns for a stock"""
    stock_data = data_service.get_stock_data(symbol, period)
    if "error" in stock_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    history = stock_data.get("history", [])
    if not history:
        raise HTTPException(status_code=404, detail="No historical data available")
    
    patterns = pattern_service.detect_candlestick_patterns(history)
    
    # Find recent patterns (non-zero values in last 30 days)
    recent_patterns = {}
    for pattern_name, values in patterns.items():
        recent_signals = []
        for i, value in enumerate(values[-30:], start=len(values)-30):
            if value != 0:
                recent_signals.append({
                    'date': history[i]['Date'],
                    'signal': 'bullish' if value > 0 else 'bearish',
                    'strength': abs(value)
                })
        if recent_signals:
            recent_patterns[pattern_name] = recent_signals
    
    return {
        'symbol': symbol,
        'patterns': recent_patterns
    }

@router.get("/{symbol}/support-resistance")
async def get_support_resistance(symbol: str, period: str = "6mo"):
    """Get support and resistance levels"""
    stock_data = data_service.get_stock_data(symbol, period)
    if "error" in stock_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    history = stock_data.get("history", [])
    if not history:
        raise HTTPException(status_code=404, detail="No historical data available")
    
    close_prices = [item["Close"] for item in history]
    levels = pattern_service.detect_support_resistance(close_prices)
    
    return {
        'symbol': symbol,
        'current_price': close_prices[-1],
        'levels': levels
    }

@router.get("/{symbol}/trends")
async def get_trend_lines(symbol: str, period: str = "6mo"):
    """Get trend lines"""
    stock_data = data_service.get_stock_data(symbol, period)
    if "error" in stock_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    history = stock_data.get("history", [])
    if not history:
        raise HTTPException(status_code=404, detail="No historical data available")
    
    close_prices = [item["Close"] for item in history]
    dates = [item["Date"] for item in history]
    
    trend_lines = pattern_service.detect_trend_lines(close_prices, dates)
    
    return {
        'symbol': symbol,
        'trend_lines': trend_lines
    }