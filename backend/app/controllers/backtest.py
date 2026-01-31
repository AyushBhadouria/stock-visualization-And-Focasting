"""
Backtesting API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.services.backtesting_service import BacktestingEngine

router = APIRouter(prefix="/api/backtest", tags=["backtest"])


class BacktestRequest(BaseModel):
    symbol: str
    start_date: str  # YYYY-MM-DD
    end_date: str    # YYYY-MM-DD
    strategy: str    # "rsi", "sma_crossover"
    initial_capital: float = 100000
    
    # Optional parameters for strategies
    rsi_oversold: Optional[int] = 30
    rsi_overbought: Optional[int] = 70
    sma_fast: Optional[int] = 50
    sma_slow: Optional[int] = 200


@router.post("/run")
async def run_backtest(request: BacktestRequest):
    """Run a backtest with specified strategy"""
    try:
        if request.strategy == "rsi":
            result = BacktestingEngine.backtest_rsi_strategy(
                request.symbol,
                request.start_date,
                request.end_date,
                request.rsi_oversold or 30,
                request.rsi_overbought or 70,
                request.initial_capital
            )
        elif request.strategy == "sma_crossover":
            result = BacktestingEngine.backtest_sma_crossover(
                request.symbol,
                request.start_date,
                request.end_date,
                request.sma_fast or 50,
                request.sma_slow or 200,
                request.initial_capital
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown strategy: {request.strategy}")
        
        return {
            "symbol": request.symbol,
            "strategy": request.strategy,
            "period": {"start": request.start_date, "end": request.end_date},
            "result": result.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rsi-strategy/{symbol}")
async def backtest_rsi(
    symbol: str,
    start_date: str = Query(..., description="Start date YYYY-MM-DD"),
    end_date: str = Query(..., description="End date YYYY-MM-DD"),
    rsi_oversold: int = Query(30, ge=10, le=50),
    rsi_overbought: int = Query(70, ge=50, le=90),
    initial_capital: float = Query(100000, ge=1000)
):
    """Backtest RSI strategy"""
    try:
        result = BacktestingEngine.backtest_rsi_strategy(
            symbol, start_date, end_date,
            rsi_oversold, rsi_overbought,
            initial_capital
        )
        
        return {
            "symbol": symbol,
            "strategy": "RSI",
            "parameters": {
                "oversold": rsi_oversold,
                "overbought": rsi_overbought
            },
            "result": result.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sma-crossover/{symbol}")
async def backtest_sma(
    symbol: str,
    start_date: str = Query(..., description="Start date YYYY-MM-DD"),
    end_date: str = Query(..., description="End date YYYY-MM-DD"),
    fast_period: int = Query(50, ge=10, le=100),
    slow_period: int = Query(200, ge=50, le=500),
    initial_capital: float = Query(100000, ge=1000)
):
    """Backtest SMA crossover strategy"""
    try:
        result = BacktestingEngine.backtest_sma_crossover(
            symbol, start_date, end_date,
            fast_period, slow_period,
            initial_capital
        )
        
        return {
            "symbol": symbol,
            "strategy": "SMA Crossover",
            "parameters": {
                "fast_period": fast_period,
                "slow_period": slow_period
            },
            "result": result.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare-strategies/{symbol}")
async def compare_strategies(
    symbol: str,
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    """Compare multiple strategies on same stock"""
    try:
        rsi_result = BacktestingEngine.backtest_rsi_strategy(symbol, start_date, end_date)
        sma_result = BacktestingEngine.backtest_sma_crossover(symbol, start_date, end_date)
        
        return {
            "symbol": symbol,
            "period": {"start": start_date, "end": end_date},
            "strategies": {
                "rsi": {
                    "metrics": rsi_result.calculate_metrics(),
                    "trades": len(rsi_result.trades)
                },
                "sma_crossover": {
                    "metrics": sma_result.calculate_metrics(),
                    "trades": len(sma_result.trades)
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
