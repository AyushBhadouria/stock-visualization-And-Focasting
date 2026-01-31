from fastapi import APIRouter
from app.services.news_service import NewsService

router = APIRouter()
news_service = NewsService()

@router.get("/market")
async def get_market_news(limit: int = 20):
    """Get general market news"""
    news = news_service.get_market_news(limit)
    return {'news': news}

@router.get("/{symbol}")
async def get_stock_news(symbol: str, limit: int = 10):
    """Get news for a specific stock"""
    news = news_service.get_stock_news(symbol.upper(), limit)
    return {
        'symbol': symbol.upper(),
        'news': news
    }