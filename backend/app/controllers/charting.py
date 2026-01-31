"""
Advanced Charting API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.charting_service import ChartingService

router = APIRouter(prefix="/api/charting", tags=["charting"])


@router.get("/candlesticks/{symbol}")
async def get_candlesticks(
    symbol: str,
    period: str = Query("1mo", description="Time period"),
    interval: str = Query("1d", description="Data interval")
):
    """Get candlestick data for charting"""
    try:
        symbol = symbol.upper().strip()
        
        # Validate period
        valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
        if period not in valid_periods:
            raise ValueError(f"Invalid period: {period}")
        
        data = ChartingService.get_candlestick_data(symbol, period)
        
        if not data:
            raise HTTPException(status_code=404, detail=f"No data found for {symbol}")
        
        return {"symbol": symbol, "data": data, "count": len(data)}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_candlesticks: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching candlestick data: {str(e)}")


@router.get("/heikin-ashi/{symbol}")
async def get_heikin_ashi(symbol: str, period: str = Query("1mo")):
    """Get Heikin Ashi candlesticks"""
    try:
        data = ChartingService.get_heikin_ashi(symbol, period)
        return {"symbol": symbol, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare")
async def compare_stocks(symbols: List[str]):
    """Compare multiple stocks on same chart"""
    try:
        if len(symbols) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 symbols")
        if len(symbols) > 5:
            raise HTTPException(status_code=400, detail="Maximum 5 symbols allowed")
        
        data = ChartingService.compare_stocks(symbols)
        return {"symbols": symbols, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fibonacci/{symbol}")
async def get_fibonacci(symbol: str, period: str = Query("1mo")):
    """Get Fibonacci retracement levels"""
    try:
        levels = ChartingService.get_fibonacci_levels(symbol, period)
        return {"symbol": symbol, "levels": levels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pivot-points/{symbol}")
async def get_pivot_points(symbol: str):
    """Get daily pivot points"""
    try:
        points = ChartingService.get_pivot_points(symbol)
        return {"symbol": symbol, "points": points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/support-resistance/{symbol}")
async def get_support_resistance(
    symbol: str,
    period: str = Query("1mo"),
    num_levels: int = Query(3, ge=1, le=5)
):
    """Get support and resistance levels"""
    try:
        levels = ChartingService.get_support_resistance(symbol, period, num_levels)
        return {"symbol": symbol, "levels": levels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/channels/{symbol}")
async def get_channels(
    symbol: str,
    period: str = Query("1mo"),
    window: int = Query(20, ge=5, le=50)
):
    """Get Donchian channels"""
    try:
        channels = ChartingService.calculate_channels(symbol, period, window)
        return {"symbol": symbol, "channels": channels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
