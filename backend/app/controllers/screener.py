"""
Stock Screener API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.screener_service import ScreenerService

router = APIRouter(prefix="/api/screener", tags=["screener"])


@router.get("/stock-info/{symbol}")
async def get_stock_info(symbol: str):
    """Get comprehensive stock information"""
    try:
        info = ScreenerService.get_stock_info(symbol)
        if not info:
            raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/screen")
async def screen_stocks(
    symbols: List[str] = Query(..., description="List of stock symbols to screen"),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    market_cap_min: Optional[int] = Query(None),
    pe_ratio_max: Optional[float] = Query(None),
    min_volume: Optional[int] = Query(None),
    rsi_oversold: Optional[bool] = Query(None),
    rsi_overbought: Optional[bool] = Query(None),
    sma_crossover: Optional[str] = Query(None)
):
    """
    Screen stocks based on multiple criteria
    
    Example: /screen?symbols=AAPL&symbols=MSFT&price_min=100&price_max=200&sma_crossover=bullish
    """
    try:
        criteria = {
            "price_min": price_min,
            "price_max": price_max,
            "market_cap_min": market_cap_min,
            "pe_ratio_max": pe_ratio_max,
            "min_volume": min_volume,
            "rsi_oversold": rsi_oversold,
            "rsi_overbought": rsi_overbought,
            "sma_crossover": sma_crossover
        }
        
        # Remove None values
        criteria = {k: v for k, v in criteria.items() if v is not None}
        
        results = ScreenerService.screen_by_criteria(symbols, criteria)
        
        return {
            "criteria": criteria,
            "total_screened": len(symbols),
            "matches": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rsi/{symbol}")
async def get_rsi(symbol: str, period: int = Query(14, ge=5, le=50)):
    """Get current RSI for a stock"""
    try:
        rsi = ScreenerService.calculate_rsi(symbol, period)
        if rsi is None:
            raise HTTPException(status_code=404, detail=f"Could not calculate RSI for {symbol}")
        
        return {
            "symbol": symbol,
            "rsi": float(rsi),
            "period": period,
            "signal": "oversold" if rsi < 30 else ("overbought" if rsi > 70 else "neutral")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sma-crossover/{symbol}")
async def get_sma_crossover(
    symbol: str,
    fast: int = Query(50),
    slow: int = Query(200)
):
    """Check SMA crossover status"""
    try:
        data = ScreenerService.calculate_sma_50_200(symbol)
        if not data:
            raise HTTPException(status_code=404, detail=f"Could not calculate SMAs for {symbol}")
        
        return {
            "symbol": symbol,
            "sma_50": data.get("sma_50"),
            "sma_200": data.get("sma_200"),
            "crossover": data.get("crossover")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-gainers")
async def get_top_gainers(limit: int = Query(10, ge=1, le=50)):
    """Get top gaining stocks (mock implementation)"""
    try:
        # This would typically pull from a real-time data source
        return {
            "type": "gainers",
            "limit": limit,
            "stocks": []  # Would be populated with real data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-losers")
async def get_top_losers(limit: int = Query(10, ge=1, le=50)):
    """Get top losing stocks (mock implementation)"""
    try:
        return {
            "type": "losers",
            "limit": limit,
            "stocks": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/most-active")
async def get_most_active(limit: int = Query(10, ge=1, le=50)):
    """Get most active stocks by volume (mock implementation)"""
    try:
        return {
            "type": "most_active",
            "limit": limit,
            "stocks": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
