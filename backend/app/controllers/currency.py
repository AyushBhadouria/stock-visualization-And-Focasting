from fastapi import APIRouter
from app.services.currency_service import CurrencyService

router = APIRouter()
currency_service = CurrencyService()

@router.get("/")
async def get_supported_currencies():
    """Get list of supported currencies"""
    return {"currencies": currency_service.get_supported_currencies()}

@router.get("/convert")
async def convert_currency(amount: float, from_currency: str = "USD", to_currency: str = "INR"):
    """Convert currency"""
    if from_currency != "USD":
        # Convert to USD first
        usd_amount = amount / currency_service.exchange_rates.get(from_currency, 1.0)
    else:
        usd_amount = amount
    
    converted_amount = currency_service.convert_price(usd_amount, to_currency)
    
    return {
        "original_amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "converted_amount": round(converted_amount, 2),
        "exchange_rate": currency_service.exchange_rates.get(to_currency, 1.0)
    }