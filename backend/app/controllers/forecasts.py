from fastapi import APIRouter, Depends, HTTPException
from app.services.forecast_service import ForecastService
from app.services.data_service import DataService
from app.controllers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()
forecast_service = ForecastService()
data_service = DataService()

class ForecastRequest(BaseModel):
    model: str = "ensemble"  # linear, arima, prophet, ensemble
    days: int = 30

@router.post("/{symbol}")
async def generate_forecast(
    symbol: str, 
    request: ForecastRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate price forecast for a stock"""
    # Get historical data
    stock_data = data_service.get_stock_data(symbol, "2y")  # More data for better forecasting
    if "error" in stock_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    history = stock_data.get("history", [])
    if not history or len(history) < 30:
        raise HTTPException(status_code=400, detail="Insufficient historical data for forecasting")
    
    # Extract prices and dates
    prices = [item["Close"] for item in history]
    dates = [item["Date"] for item in history]
    
    # Generate forecast based on model type
    if request.model == "linear":
        forecast = forecast_service.linear_regression_forecast(prices, request.days)
    elif request.model == "arima":
        forecast = forecast_service.arima_forecast(prices, request.days)
    elif request.model == "moving_average":
        forecast = forecast_service.simple_moving_average_forecast(prices, request.days)
    elif request.model == "ensemble":
        forecast = forecast_service.ensemble_forecast(dates, prices, request.days)
    else:
        raise HTTPException(status_code=400, detail="Invalid model type")
    
    if "error" in forecast:
        raise HTTPException(status_code=500, detail=f"Forecast generation failed: {forecast['error']}")
    
    return {
        "symbol": symbol,
        "current_price": prices[-1],
        "forecast": forecast,
        "generated_by": current_user["email"]
    }

@router.get("/{symbol}/models")
async def get_available_models():
    """Get list of available forecasting models"""
    return {
        "models": [
            {
                "name": "linear",
                "description": "Linear Regression - Simple trend-based forecast",
                "accuracy": "Low",
                "speed": "Fast"
            },
            {
                "name": "arima",
                "description": "ARIMA - Time series analysis model",
                "accuracy": "Medium",
                "speed": "Medium"
            },
            {
                "name": "moving_average",
                "description": "Moving Average - Simple average-based forecast",
                "accuracy": "Medium",
                "speed": "Fast"
            },
            {
                "name": "ensemble",
                "description": "Ensemble - Combination of multiple models",
                "accuracy": "Highest",
                "speed": "Slowest"
            }
        ]
    }