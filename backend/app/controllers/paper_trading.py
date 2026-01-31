"""
Paper Trading API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.services.paper_trading_service import PaperTradingService

router = APIRouter(prefix="/api/paper-trading", tags=["paper-trading"])

# Global paper trading instance (in production, would be per-user)
paper_trading = PaperTradingService(initial_cash=100000)


class TradeRequest(BaseModel):
    symbol: str
    quantity: int
    price: float
    order_id: Optional[str] = None


class PositionSizingRequest(BaseModel):
    account_risk_percent: float = 2.0
    symbol: Optional[str] = None


@router.post("/buy")
async def buy(trade: TradeRequest):
    """Place a buy order"""
    try:
        order = paper_trading.buy(
            trade.symbol,
            trade.quantity,
            trade.price,
            trade.order_id
        )
        
        if order is None:
            raise HTTPException(status_code=400, detail="Insufficient cash for this trade")
        
        return {
            "success": True,
            "order": order.to_dict(),
            "portfolio_value": paper_trading.get_portfolio_value()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sell")
async def sell(trade: TradeRequest):
    """Place a sell order"""
    try:
        order = paper_trading.sell(
            trade.symbol,
            trade.quantity,
            trade.price,
            trade.order_id
        )
        
        if order is None:
            raise HTTPException(status_code=400, detail="Insufficient position to sell")
        
        return {
            "success": True,
            "order": order.to_dict(),
            "portfolio_value": paper_trading.get_portfolio_value()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/portfolio-value")
async def get_portfolio_value():
    """Get current portfolio value and performance"""
    try:
        return paper_trading.get_portfolio_value()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/positions")
async def get_positions():
    """Get current open positions"""
    try:
        return {
            "positions": paper_trading.get_positions(),
            "total_value": paper_trading.get_portfolio_value()["total_value"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trade-history")
async def get_trade_history():
    """Get trade history with P&L"""
    try:
        return {
            "trades": paper_trading.get_trade_history(),
            "total_trades": len(paper_trading.get_trade_history())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance")
async def get_performance():
    """Get performance metrics"""
    try:
        metrics = paper_trading.get_performance_metrics()
        portfolio = paper_trading.get_portfolio_value()
        
        return {
            "portfolio": portfolio,
            "metrics": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/position-sizing")
async def position_sizing(request: PositionSizingRequest):
    """Calculate position sizes based on risk"""
    try:
        result = paper_trading.position_sizing(
            request.account_risk_percent,
            request.symbol
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_account(initial_cash: float = Query(100000, ge=1000)):
    """Reset paper trading account"""
    try:
        global paper_trading
        paper_trading = PaperTradingService(initial_cash=initial_cash)
        return {
            "success": True,
            "message": f"Account reset with ${initial_cash:,.2f}",
            "portfolio": paper_trading.get_portfolio_value()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
