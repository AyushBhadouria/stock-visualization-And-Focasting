"""
Advanced Indicators API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from app.services.advanced_indicators import AdvancedIndicatorsService

router = APIRouter(prefix="/api/indicators", tags=["indicators"])


@router.get("/atr/{symbol}")
async def get_atr(symbol: str, period: int = Query(14, ge=5, le=50)):
    """Average True Range - volatility indicator"""
    try:
        data = AdvancedIndicatorsService.calculate_atr(symbol, period)
        return {"symbol": symbol, "indicator": "ATR", "period": period, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/adx/{symbol}")
async def get_adx(symbol: str, period: int = Query(14, ge=5, le=50)):
    """Average Directional Index - trend strength"""
    try:
        data = AdvancedIndicatorsService.calculate_adx(symbol, period)
        return {"symbol": symbol, "indicator": "ADX", "period": period, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ichimoku/{symbol}")
async def get_ichimoku(symbol: str):
    """Ichimoku Cloud indicator"""
    try:
        data = AdvancedIndicatorsService.calculate_ichimoku(symbol)
        return {"symbol": symbol, "indicator": "Ichimoku", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/obv/{symbol}")
async def get_obv(symbol: str):
    """On Balance Volume"""
    try:
        data = AdvancedIndicatorsService.calculate_obv(symbol)
        return {"symbol": symbol, "indicator": "OBV", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vwap/{symbol}")
async def get_vwap(symbol: str):
    """Volume Weighted Average Price"""
    try:
        data = AdvancedIndicatorsService.calculate_vwap(symbol)
        return {"symbol": symbol, "indicator": "VWAP", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/macd/{symbol}")
async def get_macd(
    symbol: str,
    fast: int = Query(12, ge=5, le=30),
    slow: int = Query(26, ge=10, le=50),
    signal: int = Query(9, ge=5, le=20)
):
    """MACD - Moving Average Convergence Divergence"""
    try:
        data = AdvancedIndicatorsService.calculate_macd(symbol, fast, slow, signal)
        return {"symbol": symbol, "indicator": "MACD", "parameters": {"fast": fast, "slow": slow, "signal": signal}, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stochastic/{symbol}")
async def get_stochastic(
    symbol: str,
    period: int = Query(14, ge=5, le=50),
    smooth_k: int = Query(3, ge=1, le=10),
    smooth_d: int = Query(3, ge=1, le=10)
):
    """Stochastic Oscillator"""
    try:
        data = AdvancedIndicatorsService.calculate_stochastic(symbol, period, smooth_k, smooth_d)
        return {"symbol": symbol, "indicator": "Stochastic", "parameters": {"period": period, "smooth_k": smooth_k, "smooth_d": smooth_d}, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bollinger-bands/{symbol}")
async def get_bollinger_bands(
    symbol: str,
    period: int = Query(20, ge=5, le=50),
    std_dev: float = Query(2.0, ge=0.5, le=4.0)
):
    """Bollinger Bands"""
    try:
        data = AdvancedIndicatorsService.calculate_bollinger_bands(symbol, period, std_dev)
        return {"symbol": symbol, "indicator": "Bollinger Bands", "parameters": {"period": period, "std_dev": std_dev}, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
