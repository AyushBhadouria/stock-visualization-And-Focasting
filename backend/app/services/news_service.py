import requests
from typing import List, Dict
import os
from datetime import datetime, timedelta

class NewsService:
    def __init__(self):
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        self.finnhub_key = os.getenv("FINNHUB_KEY")
    
    def get_stock_news(self, symbol: str, limit: int = 10) -> List[Dict]:
        """Get news for a specific stock"""
        news = []
        
        # Try Finnhub first
        if self.finnhub_key:
            finnhub_news = self._get_finnhub_news(symbol, limit)
            news.extend(finnhub_news)
        
        # Fallback to NewsAPI
        if len(news) < limit and self.newsapi_key:
            newsapi_news = self._get_newsapi_stock_news(symbol, limit - len(news))
            news.extend(newsapi_news)
        
        return news[:limit]
    
    def get_market_news(self, limit: int = 20) -> List[Dict]:
        """Get general market news"""
        if not self.newsapi_key:
            return self._get_mock_news()
        
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': 'stock market OR finance OR economy',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': limit,
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._format_newsapi_articles(data.get('articles', []))
            
        except Exception as e:
            print(f"Error fetching market news: {e}")
        
        return self._get_mock_news()
    
    def _get_finnhub_news(self, symbol: str, limit: int) -> List[Dict]:
        """Get news from Finnhub API"""
        try:
            url = f"https://finnhub.io/api/v1/company-news"
            params = {
                'symbol': symbol,
                'from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'to': datetime.now().strftime('%Y-%m-%d'),
                'token': self.finnhub_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                articles = response.json()
                return self._format_finnhub_articles(articles[:limit])
                
        except Exception as e:
            print(f"Error fetching Finnhub news: {e}")
        
        return []
    
    def _get_newsapi_stock_news(self, symbol: str, limit: int) -> List[Dict]:
        """Get stock news from NewsAPI"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': f'{symbol} stock',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': limit,
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._format_newsapi_articles(data.get('articles', []))
                
        except Exception as e:
            print(f"Error fetching NewsAPI stock news: {e}")
        
        return []
    
    def _format_finnhub_articles(self, articles: List[Dict]) -> List[Dict]:
        """Format Finnhub articles"""
        formatted = []
        for article in articles:
            formatted.append({
                'title': article.get('headline', ''),
                'description': article.get('summary', ''),
                'url': article.get('url', ''),
                'source': article.get('source', 'Finnhub'),
                'published_at': datetime.fromtimestamp(article.get('datetime', 0)).isoformat(),
                'image_url': article.get('image', '')
            })
        return formatted
    
    def _format_newsapi_articles(self, articles: List[Dict]) -> List[Dict]:
        """Format NewsAPI articles"""
        formatted = []
        for article in articles:
            formatted.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', 'NewsAPI'),
                'published_at': article.get('publishedAt', ''),
                'image_url': article.get('urlToImage', '')
            })
        return formatted
    
    def _get_mock_news(self) -> List[Dict]:
        """Return mock news when APIs are not available"""
        return [
            {
                'title': 'Stock Market Reaches New Highs',
                'description': 'Major indices continue their upward trend amid positive economic data.',
                'url': '#',
                'source': 'Mock News',
                'published_at': datetime.now().isoformat(),
                'image_url': ''
            },
            {
                'title': 'Tech Stocks Lead Market Rally',
                'description': 'Technology companies show strong earnings growth this quarter.',
                'url': '#',
                'source': 'Mock News',
                'published_at': (datetime.now() - timedelta(hours=2)).isoformat(),
                'image_url': ''
            }
        ]