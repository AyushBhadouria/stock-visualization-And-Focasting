import requests
from typing import Dict
import os

class CurrencyService:
    def __init__(self):
        self.exchange_rates = {
            'USD': 1.0,
            'INR': 83.12,  # Indian Rupee
            'CNY': 7.24,   # Chinese Yuan
            'AED': 3.67,   # UAE Dirham
            'EUR': 0.92,   # Euro
            'GBP': 0.79,   # British Pound
            'JPY': 149.50, # Japanese Yen
        }
    
    def convert_price(self, usd_price: float, target_currency: str) -> float:
        """Convert USD price to target currency"""
        if target_currency == 'USD':
            return usd_price
        
        rate = self.exchange_rates.get(target_currency, 1.0)
        return usd_price * rate
    
    def get_currency_symbol(self, currency: str) -> str:
        """Get currency symbol"""
        symbols = {
            'USD': '$',
            'INR': '₹',
            'CNY': '¥',
            'AED': 'د.إ',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
        }
        return symbols.get(currency, '$')
    
    def get_supported_currencies(self) -> Dict:
        """Get list of supported currencies"""
        return {
            'USD': {'name': 'US Dollar', 'symbol': '$'},
            'INR': {'name': 'Indian Rupee', 'symbol': '₹'},
            'CNY': {'name': 'Chinese Yuan', 'symbol': '¥'},
            'AED': {'name': 'UAE Dirham', 'symbol': 'د.إ'},
            'EUR': {'name': 'Euro', 'symbol': '€'},
            'GBP': {'name': 'British Pound', 'symbol': '£'},
            'JPY': {'name': 'Japanese Yen', 'symbol': '¥'},
        }