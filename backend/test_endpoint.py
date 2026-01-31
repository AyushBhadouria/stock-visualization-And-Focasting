@router.get("/test/{symbol}")
async def test_stock_data(symbol: str):
    """Test endpoint to check yfinance"""
    try:
        import yfinance as yf
        print(f"Testing yfinance for {symbol}")
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")
        
        print(f"History shape: {hist.shape}")
        print(f"History columns: {hist.columns.tolist()}")
        print(f"First few rows: {hist.head()}")
        
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