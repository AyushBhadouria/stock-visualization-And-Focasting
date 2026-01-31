import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Trash2, TrendingUp, TrendingDown, Eye, EyeOff } from 'lucide-react';
import { Link } from 'react-router-dom';
import { watchlistAPI } from '../services/api';
import Sparkline from '../components/Sparkline';
import SkeletonLoader from '../components/SkeletonLoader';

const Watchlist = () => {
  const queryClient = useQueryClient();
  const [sortBy, setSortBy] = useState('symbol');
  const [sortOrder, setSortOrder] = useState('asc');

  const { data: watchlistData, isLoading } = useQuery(
    'watchlist',
    watchlistAPI.getWatchlist,
    {
      select: (data) => data.data.watchlist,
    }
  );

  const removeFromWatchlistMutation = useMutation(
    watchlistAPI.removeFromWatchlist,
    {
      onSuccess: () => {
        queryClient.invalidateQueries('watchlist');
      },
    }
  );

  const handleRemove = (symbol) => {
    if (window.confirm(`Remove ${symbol} from watchlist?`)) {
      removeFromWatchlistMutation.mutate(symbol);
    }
  };

  const sortedData = React.useMemo(() => {
    if (!watchlistData) return [];
    
    const sorted = [...watchlistData].sort((a, b) => {
      let aVal, bVal;
      switch(sortBy) {
        case 'price':
          aVal = a.current_price || 0;
          bVal = b.current_price || 0;
          break;
        case 'change':
          aVal = a.change || 0;
          bVal = b.change || 0;
          break;
        case 'changePercent':
          aVal = a.change_percent || 0;
          bVal = b.change_percent || 0;
          break;
        default:
          aVal = a.symbol;
          bVal = b.symbol;
      }
      
      return sortOrder === 'asc' ? 
        (typeof aVal === 'string' ? aVal.localeCompare(bVal) : aVal - bVal) :
        (typeof aVal === 'string' ? bVal.localeCompare(aVal) : bVal - aVal);
    });
    
    return sorted;
  }, [watchlistData, sortBy, sortOrder]);

  const toggleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Watchlist</h1>
          <p className="text-gray-600 dark:text-gray-400">Track your favorite stocks</p>
        </div>
        <div className="card">
          <SkeletonLoader type="card" count={5} />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Watchlist</h1>
          <p className="text-gray-600 dark:text-gray-400">Track your favorite stocks</p>
        </div>
        {watchlistData && watchlistData.length > 0 && (
          <div className="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
            {watchlistData.length} stocks
          </div>
        )}
      </div>

      {watchlistData && watchlistData.length > 0 ? (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th 
                    onClick={() => toggleSort('symbol')}
                    className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    Symbol {sortBy === 'symbol' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th 
                    onClick={() => toggleSort('price')}
                    className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    Price {sortBy === 'price' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th 
                    onClick={() => toggleSort('change')}
                    className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    Change {sortBy === 'change' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th 
                    onClick={() => toggleSort('changePercent')}
                    className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    % Change {sortBy === 'changePercent' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                    Trend
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {sortedData.map((stock) => {
                  const isPositive = (stock.change || 0) >= 0;
                  return (
                    <tr key={stock.symbol} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-150">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Link
                          to={`/stock/${stock.symbol}`}
                          className="text-primary-600 dark:text-primary-400 hover:text-primary-900 dark:hover:text-primary-300 font-bold cursor-pointer hover:underline transition-colors"
                        >
                          {stock.symbol}
                        </Link>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 dark:text-gray-100">
                        ${stock.current_price?.toFixed(2) || 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <div className={`flex items-center font-semibold ${
                          isPositive ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'
                        }`}>
                          {isPositive ? <TrendingUp size={16} className="mr-2" /> : <TrendingDown size={16} className="mr-2" />}
                          {isPositive ? '+' : ''}{stock.change?.toFixed(2) || '0.00'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span className={`font-semibold ${
                          isPositive ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'
                        }`}>
                          {isPositive ? '+' : ''}{stock.change_percent?.toFixed(2) || '0.00'}%
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Sparkline 
                          data={[1, 1.2, 1.1, 1.3, 1.2, 1.4, isPositive ? 1.5 : 0.8]} 
                          sentiment={isPositive ? 'up' : 'down'} 
                          size="sm" 
                        />
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <button
                          onClick={() => handleRemove(stock.symbol)}
                          className="inline-flex items-center gap-2 px-3 py-2 text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors cursor-pointer"
                          disabled={removeFromWatchlistMutation.isLoading}
                          title="Remove from watchlist"
                        >
                          <Trash2 size={16} />
                          <span className="text-xs font-medium hidden sm:inline">Remove</span>
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="card text-center py-16">
          <div className="flex flex-col items-center justify-center">
            <div className="p-4 bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900/30 dark:to-primary-800/30 rounded-full mb-4">
              <TrendingUp size={48} className="text-primary-600 dark:text-primary-400" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">No stocks in watchlist</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-sm">
              Build your watchlist by searching for stocks and adding them to track their performance.
            </p>
            <Link to="/" className="btn-primary">
              Browse Stocks
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default Watchlist;