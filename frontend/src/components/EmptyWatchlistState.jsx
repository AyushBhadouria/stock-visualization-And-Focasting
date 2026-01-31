import React from 'react';
import { Plus, Search, TrendingUp } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const EmptyWatchlistState = () => {
  const navigate = useNavigate();

  const suggestedStocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA'];

  return (
    <div className="text-center py-12">
      <div className="mb-4 flex justify-center">
        <div className="p-3 bg-gradient-to-br from-primary-100 to-primary-200 rounded-full">
          <TrendingUp className="h-8 w-8 text-primary-600" />
        </div>
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Build Your Watchlist</h3>
      <p className="text-gray-600 mb-6 max-w-sm mx-auto">
        Start tracking stocks and stay updated with real-time data and insights
      </p>
      
      <button
        onClick={() => {
          // Focus the search bar
          const searchInput = document.querySelector('input[placeholder*="Search"]');
          if (searchInput) searchInput.focus();
        }}
        className="inline-flex items-center justify-center px-4 py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors mb-6 gap-2"
      >
        <Plus size={18} />
        Add Your First Stock
      </button>

      <div className="mt-8">
        <p className="text-sm font-medium text-gray-700 mb-3">Popular Stocks</p>
        <div className="flex flex-wrap gap-2 justify-center">
          {suggestedStocks.map((symbol) => (
            <button
              key={symbol}
              onClick={() => navigate(`/stock/${symbol}`)}
              className="px-3 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200 transition-colors flex items-center gap-1"
            >
              {symbol}
              <Plus size={14} className="opacity-60" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EmptyWatchlistState;
