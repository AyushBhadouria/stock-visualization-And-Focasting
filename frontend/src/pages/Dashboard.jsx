import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { TrendingUp, TrendingDown, Activity, Plus, Bell, BarChart3, Zap, AlertCircle } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { watchlistAPI } from '../services/api';
import Sparkline from '../components/Sparkline';
import SkeletonLoader from '../components/SkeletonLoader';
import EmptyWatchlistState from '../components/EmptyWatchlistState';

const Dashboard = () => {
  const navigate = useNavigate();
  const [isLiveUpdating, setIsLiveUpdating] = useState(true);
  
  const { data: watchlistData, isLoading } = useQuery(
    'watchlist',
    watchlistAPI.getWatchlist,
    {
      select: (data) => data.data.watchlist,
    }
  );

  // Simulate live data pulse
  useEffect(() => {
    const interval = setInterval(() => {
      setIsLiveUpdating(prev => !prev);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const portfolioValue = 125430.50;
  const portfolioChange = 2345.75;
  const portfolioChangePercent = 1.89;

  const marketMovers = [
    { symbol: 'AAPL', name: 'Apple Inc.', price: 175.43, change: 2.34, changePercent: 1.35, sparkData: [1, 1.5, 1.2, 1.8, 1.5, 2, 1.8, 2.2, 2, 2.3] },
    { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 2847.63, change: -15.23, changePercent: -0.53, sparkData: [1.5, 1.3, 1.4, 1.2, 1.1, 1, 0.9, 0.8, 0.9, 0.8] },
    { symbol: 'MSFT', name: 'Microsoft Corp.', price: 378.85, change: 4.12, changePercent: 1.10, sparkData: [1, 1.2, 1.3, 1.5, 1.4, 1.6, 1.7, 1.9, 1.8, 2] },
    { symbol: 'TSLA', name: 'Tesla Inc.', price: 248.50, change: -8.75, changePercent: -3.40, sparkData: [2, 1.9, 1.7, 1.5, 1.3, 1.2, 1, 0.9, 0.7, 0.5] },
  ];

  return (
    <div className="space-y-8">
      {/* Header with Live Indicator */}
      <div className="flex items-center justify-between pt-2">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">Dashboard</h1>
          <div className="flex items-center gap-3">
            <div className={`flex items-center gap-2 text-sm font-medium ${isLiveUpdating ? 'text-green-600 dark:text-green-400' : 'text-gray-600 dark:text-gray-400'}`}>
              <div className={`w-2.5 h-2.5 rounded-full ${isLiveUpdating ? 'bg-green-600 dark:bg-green-400 animate-pulse shadow-lg shadow-green-500' : 'bg-gray-400 dark:bg-gray-500'}`}></div>
              {isLiveUpdating ? '● Live Updates' : '○ Data Cached'}
            </div>
            <span className="text-gray-600 dark:text-gray-400 text-sm">Welcome to your stock analysis platform</span>
          </div>
        </div>
      </div>

      {/* Main Hero Card - Portfolio Value */}
      <div className="card bg-gradient-to-br from-primary-600 to-primary-700 text-white shadow-lg hover:shadow-xl transition-shadow">
        <div className="flex items-start justify-between mb-8">
          <div className="flex-1">
            <p className="text-primary-100 text-xs font-semibold uppercase tracking-wide mb-2">Total Portfolio Value</p>
            <p className="text-5xl font-bold mb-1">${portfolioValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
            <p className="text-primary-100 text-sm">Across all holdings</p>
          </div>
          <div className="text-right">
            <p className={`text-2xl font-bold ${portfolioChange >= 0 ? 'text-emerald-300' : 'text-red-300'}`}>
              {portfolioChange >= 0 ? '+' : ''}{portfolioChange.toFixed(2)}
            </p>
            <p className={`text-sm font-semibold ${portfolioChange >= 0 ? 'text-emerald-300' : 'text-red-300'}`}>
              {portfolioChange >= 0 ? '+' : ''}{portfolioChangePercent.toFixed(2)}%
            </p>
          </div>
        </div>
        <div className="flex items-center justify-between pt-4 border-t border-primary-500/30">
          <div className="text-primary-100 text-xs">Last updated: Just now</div>
          <Sparkline data={[1, 1.3, 1.2, 1.5, 1.4, 1.6, 1.8, 1.7, 2, 2.2]} sentiment="up" size="lg" />
        </div>
      </div>

      {/* Market Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* S&P 500 */}
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-2">S&P 500</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">4,567.89</p>
              <p className="text-sm font-bold text-emerald-600 dark:text-emerald-400 mt-1">+1.23%</p>
            </div>
            <Sparkline data={[1, 1.5, 1.3, 1.8, 1.6, 2, 1.9, 2.2, 2.1, 2.3]} sentiment="up" size="md" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-2">NASDAQ</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">14,234.56</p>
              <p className="text-sm font-bold text-red-600 dark:text-red-400 mt-1">-0.45%</p>
            </div>
            <Sparkline data={[1.5, 1.3, 1.4, 1.2, 1.1, 1, 0.9, 0.8, 0.9, 0.8]} sentiment="down" size="md" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-2">DOW JONES</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">35,678.90</p>
              <p className="text-sm font-bold text-blue-600 dark:text-blue-400 mt-1">+0.78%</p>
            </div>
            <Sparkline data={[1, 1.2, 1.3, 1.5, 1.4, 1.6, 1.7, 1.9, 1.8, 2]} sentiment="up" size="md" />
          </div>
        </div>
      </div>

      {/* Watchlist and Market Movers */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Watchlist */}
        <div className="card">
          <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Your Watchlist</h2>
            {watchlistData && watchlistData.length > 0 && (
              <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded text-xs font-medium">
                {watchlistData.length} stocks
              </span>
            )}
          </div>
          
          {isLoading ? (
            <SkeletonLoader type="card" count={5} />
          ) : watchlistData && watchlistData.length > 0 ? (
            <div className="space-y-3">
              {watchlistData.slice(0, 5).map((stock) => (
                <div
                  key={stock.symbol}
                  className="group flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 hover:shadow-md cursor-pointer transition-all duration-200 border border-transparent hover:border-primary-300 dark:hover:border-primary-600"
                >
                  <div 
                    className="flex-1 text-left"
                    onClick={() => navigate(`/stock/${stock.symbol}`)}
                  >
                    <p className="font-bold text-gray-900 dark:text-white text-base">{stock.symbol}</p>
                    <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">${stock.current_price?.toFixed(2) || 'N/A'}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <p className={`text-sm font-bold ${
                        (stock.change || 0) >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                      }`}>
                        {(stock.change || 0) >= 0 ? '+' : ''}{stock.change?.toFixed(2) || '0.00'}
                      </p>
                      <p className={`text-xs font-semibold ${
                        (stock.change_percent || 0) >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                      }`}>
                        {(stock.change_percent || 0) >= 0 ? '+' : ''}{stock.change_percent?.toFixed(2) || '0.00'}%
                      </p>
                    </div>
                    <button
                      onClick={() => navigate(`/stock/${stock.symbol}`)}
                      className="p-1 opacity-0 group-hover:opacity-100 bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 rounded hover:bg-primary-200 dark:hover:bg-primary-800 transition-all duration-200"
                      title="View details"
                    >
                      <TrendingUp size={16} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <EmptyWatchlistState />
          )}
        </div>

        {/* Market Movers */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">Market Movers</h2>
          <div className="space-y-2">
            {marketMovers.map((stock) => (
              <div
                key={stock.symbol}
                className="group flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 hover:shadow-md transition-all duration-200 border border-transparent hover:border-primary-300 dark:hover:border-primary-600"
              >
                <div 
                  className="flex-1 cursor-pointer"
                  onClick={() => navigate(`/stock/${stock.symbol}`)}
                >
                  <p className="font-bold text-gray-900 dark:text-white text-base">{stock.symbol}</p>
                  <p className="text-xs text-gray-600 dark:text-gray-500 mt-1">{stock.name}</p>
                </div>
                <div className="flex items-center gap-3">
                  <Sparkline 
                    data={[1, 1.2, 1.1, 1.3, 1.2, 1.4, stock.change >= 0 ? 1.5 : 0.8]} 
                    sentiment={stock.change >= 0 ? 'up' : 'down'} 
                    size="sm" 
                  />
                  <div className="text-right min-w-max">
                    <p className="text-sm font-bold text-gray-900 dark:text-white">${stock.price.toFixed(2)}</p>
                    <p className={`text-xs font-semibold ${
                      stock.change >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'
                    }`}>
                      {stock.change >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button 
            onClick={() => navigate('/stock/AAPL')}
            className="group p-5 border-2 border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 hover:bg-primary-50 dark:hover:bg-gray-700 hover:shadow-lg hover:border-primary-400 dark:hover:border-primary-500 text-left transition-all duration-200 transform hover:scale-105 hover:-translate-y-1"
          >
            <div className="flex items-start justify-between mb-3">
              <BarChart3 className="h-6 w-6 text-primary-600 dark:text-primary-400 group-hover:scale-125 transition-transform" />
            </div>
            <h3 className="font-bold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors mb-1 text-base">Stock Screener</h3>
            <p className="text-sm text-gray-600 dark:text-gray-500 leading-relaxed">Find stocks by criteria</p>
          </button>

          <button 
            onClick={() => navigate('/portfolio')}
            className="group p-5 border-2 border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 hover:bg-primary-50 dark:hover:bg-gray-700 hover:shadow-lg hover:border-primary-400 dark:hover:border-primary-500 text-left transition-all duration-200 transform hover:scale-105 hover:-translate-y-1"
          >
            <div className="flex items-start justify-between mb-3">
              <Zap className="h-6 w-6 text-primary-600 dark:text-primary-400 group-hover:scale-125 transition-transform" />
            </div>
            <h3 className="font-bold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors mb-1 text-base">Portfolio Tracker</h3>
            <p className="text-sm text-gray-600 dark:text-gray-500 leading-relaxed">Track investments</p>
          </button>

          <button 
            onClick={() => {
              const searchInput = document.querySelector('input[placeholder*="Search"]');
              if (searchInput) {
                searchInput.focus();
                searchInput.setAttribute('data-hint', 'Search for a stock, then click Price Alerts');
              }
            }}
            className="group p-5 border-2 border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 hover:bg-primary-50 dark:hover:bg-gray-700 hover:shadow-lg hover:border-primary-400 dark:hover:border-primary-500 text-left transition-all duration-200 transform hover:scale-105 hover:-translate-y-1"
          >
            <div className="flex items-start justify-between mb-3">
              <Bell className="h-6 w-6 text-primary-600 dark:text-primary-400 group-hover:scale-125 transition-transform" />
            </div>
            <h3 className="font-bold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors mb-1 text-base">Price Alerts</h3>
            <p className="text-sm text-gray-600 dark:text-gray-500 leading-relaxed">Set up notifications</p>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;