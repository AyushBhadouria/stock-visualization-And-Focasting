import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

class ForecastService:
    
    def linear_regression_forecast(self, prices: List[float], days: int = 30) -> Dict:
        """Simple linear regression forecast"""
        try:
            X = np.array(range(len(prices))).reshape(-1, 1)
            y = np.array(prices)
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict future values
            future_X = np.array(range(len(prices), len(prices) + days)).reshape(-1, 1)
            predictions = model.predict(future_X)
            
            return {
                "model": "linear_regression",
                "predictions": predictions.tolist(),
                "confidence": 0.7,  # Simple confidence score
                "days": days
            }
        except Exception as e:
            return {"error": str(e)}
    
    def arima_forecast(self, prices: List[float], days: int = 30) -> Dict:
        """ARIMA model forecast"""
        try:
            # Simple ARIMA(1,1,1) model
            model = ARIMA(prices, order=(1, 1, 1))
            fitted_model = model.fit()
            
            forecast = fitted_model.forecast(steps=days)
            conf_int = fitted_model.get_forecast(steps=days).conf_int()
            
            return {
                "model": "arima",
                "predictions": forecast.tolist(),
                "confidence_lower": conf_int.iloc[:, 0].tolist(),
                "confidence_upper": conf_int.iloc[:, 1].tolist(),
                "days": days
            }
        except Exception as e:
            return {"error": str(e)}
    
    def prophet_forecast(self, dates: List[str], prices: List[float], days: int = 30) -> Dict:
        """Facebook Prophet forecast"""
        try:
            # Prepare data for Prophet
            df = pd.DataFrame({
                'ds': pd.to_datetime(dates),
                'y': prices
            })
            
            model = Prophet(daily_seasonality=True)
            model.fit(df)
            
            # Create future dataframe
            future = model.make_future_dataframe(periods=days)
            forecast = model.predict(future)
            
            # Get only future predictions
            future_forecast = forecast.tail(days)
            
            return {
                "model": "prophet",
                "predictions": future_forecast['yhat'].tolist(),
                "confidence_lower": future_forecast['yhat_lower'].tolist(),
                "confidence_upper": future_forecast['yhat_upper'].tolist(),
                "dates": future_forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
                "days": days
            }
        except Exception as e:
            return {"error": str(e)}
    
    def ensemble_forecast(self, dates: List[str], prices: List[float], days: int = 30) -> Dict:
        """Ensemble of multiple models"""
        try:
            lr_result = self.linear_regression_forecast(prices, days)
            arima_result = self.arima_forecast(prices, days)
            prophet_result = self.prophet_forecast(dates, prices, days)
            
            # Simple ensemble - average predictions
            if all('predictions' in result for result in [lr_result, arima_result, prophet_result]):
                ensemble_pred = np.mean([
                    lr_result['predictions'],
                    arima_result['predictions'],
                    prophet_result['predictions']
                ], axis=0)
                
                return {
                    "model": "ensemble",
                    "predictions": ensemble_pred.tolist(),
                    "individual_models": {
                        "linear_regression": lr_result,
                        "arima": arima_result,
                        "prophet": prophet_result
                    },
                    "days": days
                }
            else:
                return {"error": "One or more models failed"}
                
        except Exception as e:
            return {"error": str(e)}