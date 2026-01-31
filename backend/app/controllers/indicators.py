from fastapi import APIRouter, HTTPException
from app.services.indicator_service import IndicatorService
from app.services.data_service import DataService
from typing import List, Optional

router = APIRouter()
indicator_service = IndicatorService()
data_service = DataService()

@router.get("/{symbol}")
async def get_indicators(
    symbol: str, 
    indicators: str = "sma,rsi,macd",
    period: str = "1y"
):
    """Get technical indicators for a stock"""
    # Get stock data first
    stock_data = data_service.get_stock_data(symbol, period)
    if "error" in stock_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    history = stock_data.get("history", [])
    if not history:
        raise HTTPException(status_code=404, detail="No historical data available")
    
    # Calculate requested indicators
    requested_indicators = indicators.split(",")
    result = {"symbol": symbol, "indicators": {}}
    
    close_prices = [item["Close"] for item in history]
    high_prices = [item["High"] for item in history]
    low_prices = [item["Low"] for item in history]
    
    if "sma" in requested_indicators:
        result["indicators"]["sma_20"] = indicator_service.calculate_sma(close_prices, 20)
        result["indicators"]["sma_50"] = indicator_service.calculate_sma(close_prices, 50)
    
    if "ema" in requested_indicators:
        result["indicators"]["ema_12"] = indicator_service.calculate_ema(close_prices, 12)
        result["indicators"]["ema_26"] = indicator_service.calculate_ema(close_prices, 26)
    
    if "rsi" in requested_indicators:
        result["indicators"]["rsi"] = indicator_service.calculate_rsi(close_prices)
    
    if "macd" in requested_indicators:
        result["indicators"]["macd"] = indicator_service.calculate_macd(close_prices)
    
    if "bollinger" in requested_indicators:
        result["indicators"]["bollinger"] = indicator_service.calculate_bollinger_bands(close_prices)
    
    if "stochastic" in requested_indicators:
        result["indicators"]["stochastic"] = indicator_service.calculate_stochastic(
            high_prices, low_prices, close_prices
        )
    
    return result

@router.get("/{symbol}/all")
async def get_all_indicators(symbol: str, period: str = "1y"):
    """Get all available indicators for a stock"""
    stock_data = data_service.get_stock_data(symbol, period)
    if "error" in stock_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    history = stock_data.get("history", [])
    if not history:
        raise HTTPException(status_code=404, detail="No historical data available")
    
    indicators = indicator_service.calculate_all_indicators(history)
    
    return {
        "symbol": symbol,
        "indicators": indicators
    }