from fastapi import APIRouter, HTTPException
from app.services.data_service import DataService
from typing import Optional
import yfinance as yf

router = APIRouter()
data_service = DataService()

@router.get("/search")
async def search_stocks(query: str):
    """Search for stocks by symbol or name"""
    try:
        print(f"Searching for stocks with query: {query}")
        results = data_service.search_stocks(query)
        print(f"Search results: {len(results)} stocks found")
        return {"results": results}
    except Exception as e:
        print(f"Search error: {str(e)}")
        return {"results": []}

@router.get("/{symbol}")
async def get_stock_info(symbol: str, period: str = "1y"):
    """Get detailed stock information"""
    try:
        print(f"Getting stock info for {symbol} with period {period}")
        data = data_service.get_stock_data(symbol, period)
        print(f"Stock data result: {data.get('symbol', 'No symbol')} - {len(data.get('history', []))} records")
        
        if "error" in data:
            print(f"Stock data error: {data['error']}")
            raise HTTPException(status_code=404, detail=f"Stock {symbol} not found: {data['error']}")
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Stock info error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get stock info: {str(e)}")

@router.get("/{symbol}/quote")
async def get_stock_quote(symbol: str):
    """Get real-time stock quote"""
    quote = data_service.get_real_time_quote(symbol)
    if "error" in quote:
        raise HTTPException(status_code=404, detail=f"Quote for {symbol} not available")
    return quote

@router.get("/{symbol}/history")
async def get_stock_history(symbol: str, period: str = "1y", interval: str = "1d"):
    """Get historical stock data"""
    data = data_service.get_stock_data(symbol, period)
    if "error" in data:
        raise HTTPException(status_code=404, detail=f"History for {symbol} not available")
    return {"symbol": symbol, "history": data.get("history", [])}

@router.get("/test/{symbol}")
async def test_stock_data(symbol: str):
    """Test endpoint to check yfinance"""
    try:
        print(f"Testing yfinance for {symbol}")
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")
        
        print(f"History shape: {hist.shape}")
        print(f"History columns: {hist.columns.tolist()}")
        
        if hist.empty:
            return {"error": "No data returned from yfinance", "symbol": symbol}
        
        return {
            "symbol": symbol,
            "data_points": len(hist),
            "columns": hist.columns.tolist(),
            "first_row": hist.iloc[0].to_dict(),
            "last_row": hist.iloc[-1].to_dict()
        }
        
    except Exception as e:
        print(f"Test error: {str(e)}")
        return {"error": str(e), "symbol": symbol}