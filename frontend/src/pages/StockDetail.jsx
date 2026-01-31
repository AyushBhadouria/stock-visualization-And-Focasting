import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from 'react-query';
import { Plus, Star, TrendingUp, TrendingDown } from 'lucide-react';
import { stockAPI, indicatorAPI, forecastAPI, watchlistAPI } from '../services/api';
import StockChart from '../components/StockChart';

const StockDetail = () => {
  const { symbol } = useParams();
  const queryClient = useQueryClient();
  const [selectedPeriod, setSelectedPeriod] = useState('1y');
  const [selectedIndicators, setSelectedIndicators] = useState(['sma', 'rsi']);
  const [forecastModel, setForecastModel] = useState('ensemble');
  const [forecastDays, setForecastDays] = useState(30);

  // Fetch stock data
  const { data: stockData, isLoading: stockLoading } = useQuery(
    ['stock', symbol, selectedPeriod],
    () => stockAPI.getStock(symbol, selectedPeriod),
    {
      select: (data) => data.data,
      enabled: !!symbol,
    }
  );

  // Fetch indicators
  const { data: indicatorData, isLoading: indicatorLoading } = useQuery(
    ['indicators', symbol, selectedIndicators.join(','), selectedPeriod],
    () => indicatorAPI.getIndicators(symbol, selectedIndicators.join(','), selectedPeriod),
    {
      select: (data) => data.data.indicators,
      enabled: !!symbol && selectedIndicators.length > 0,
    }
  );

  // Fetch company info
  const { data: companyData } = useQuery(
    ['company', symbol],
    () => stockAPI.getCompany(symbol),
    {
      select: (data) => data.data,
      enabled: !!symbol,
    }
  );

  // Generate forecast
  const { data: forecastData, isLoading: forecastLoading, refetch: generateForecast } = useQuery(
    ['forecast', symbol, forecastModel, forecastDays],
    () => forecastAPI.generateForecast(symbol, forecastModel, forecastDays),
    {
      select: (data) => data.data,
      enabled: false, // Manual trigger
    }
  );

  const handleAddToWatchlist = async () => {
    try {
      await watchlistAPI.addToWatchlist(symbol);
      queryClient.invalidateQueries('watchlist');
      alert('Added to watchlist!');
    } catch (error) {
      alert('Failed to add to watchlist');
    }
  };

  const periods = [
    { value: '1d', label: '1D' },
    { value: '5d', label: '5D' },
    { value: '1mo', label: '1M' },
    { value: '3mo', label: '3M' },
    { value: '6mo', label: '6M' },
    { value: '1y', label: '1Y' },
    { value: '2y', label: '2Y' },
    { value: '5y', label: '5Y' },
  ];

  const availableIndicators = [
    { value: 'sma', label: 'SMA' },
    { value: 'ema', label: 'EMA' },
    { value: 'rsi', label: 'RSI' },
    { value: 'macd', label: 'MACD' },
    { value: 'bollinger', label: 'Bollinger Bands' },
    { value: 'stochastic', label: 'Stochastic' },
  ];

  if (stockLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg">Loading stock data...</div>
      </div>
    );
  }

  if (!stockData) {
    return (
      <div className="text-center py-8">
        <h2 className="text-2xl font-bold text-gray-900">Stock not found</h2>
        <p className="text-gray-600">The symbol "{symbol}" could not be found.</p>
      </div>
    );
  }

  const currentPrice = stockData.price || 0;
  const change = stockData.change || 0;
  const changePercent = stockData.change_percent || 0;
  const isPositive = change >= 0;

  return (
    <div className="space-y-6">
      {/* Stock Header */}
      <div className="card">
        <div className="flex justify-between items-start">
          <div>
            <div className="flex items-center space-x-4">
              <h1 className="text-3xl font-bold text-gray-900">{symbol}</h1>
              <button
                onClick={handleAddToWatchlist}
                className="p-2 text-gray-400 hover:text-yellow-500"
              >
                <Star size={24} />
              </button>
            </div>
            <p className="text-lg text-gray-600">{stockData.name}</p>
            <div className="flex items-center space-x-4 mt-2">
              <span className="text-3xl font-bold text-gray-900">
                ${currentPrice.toFixed(2)}
              </span>
              <div className={`flex items-center space-x-1 ${
                isPositive ? 'text-green-600' : 'text-red-600'
              }`}>
                {isPositive ? <TrendingUp size={20} /> : <TrendingDown size={20} />}
                <span className="font-medium">
                  {isPositive ? '+' : ''}{change.toFixed(2)} ({isPositive ? '+' : ''}{changePercent.toFixed(2)}%)
                </span>
              </div>
            </div>
          </div>
          
          {/* Company Stats */}
          {companyData && (
            <div className="text-right space-y-1">
              <div className="text-sm text-gray-600">Market Cap</div>
              <div className="font-medium">
                {companyData.market_cap ? `$${(companyData.market_cap / 1e9).toFixed(2)}B` : 'N/A'}
              </div>
              <div className="text-sm text-gray-600">P/E Ratio</div>
              <div className="font-medium">{companyData.pe_ratio?.toFixed(2) || 'N/A'}</div>
            </div>
          )}
        </div>
      </div>

      {/* Chart Controls */}
      <div className="card">
        <div className="flex flex-wrap items-center justify-between gap-4">
          {/* Period Selector */}
          <div className="flex space-x-2">
            {periods.map((period) => (
              <button
                key={period.value}
                onClick={() => setSelectedPeriod(period.value)}
                className={`px-3 py-1 rounded text-sm font-medium ${
                  selectedPeriod === period.value
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {period.label}
              </button>
            ))}
          </div>

          {/* Indicator Selector */}
          <div className="flex flex-wrap gap-2">
            {availableIndicators.map((indicator) => (
              <button
                key={indicator.value}
                onClick={() => {
                  setSelectedIndicators(prev =>
                    prev.includes(indicator.value)
                      ? prev.filter(i => i !== indicator.value)
                      : [...prev, indicator.value]
                  );
                }}
                className={`px-3 py-1 rounded text-sm font-medium ${
                  selectedIndicators.includes(indicator.value)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {indicator.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Price Chart</h2>
        {stockData.history && stockData.history.length > 0 ? (
          <StockChart
            data={stockData.history}
            indicators={indicatorData || {}}
            height={500}
          />
        ) : (
          <div className="text-center py-8 text-gray-500">
            No chart data available
          </div>
        )}
      </div>

      {/* Forecast Section */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Price Forecast</h2>
        <div className="flex items-center space-x-4 mb-4">
          <select
            value={forecastModel}
            onChange={(e) => setForecastModel(e.target.value)}
            className="input"
          >
            <option value="linear">Linear Regression</option>
            <option value="arima">ARIMA</option>
            <option value="prophet">Prophet</option>
            <option value="ensemble">Ensemble</option>
          </select>
          
          <select
            value={forecastDays}
            onChange={(e) => setForecastDays(Number(e.target.value))}
            className="input"
          >
            <option value={7}>7 days</option>
            <option value={14}>14 days</option>
            <option value={30}>30 days</option>
            <option value={90}>90 days</option>
          </select>
          
          <button
            onClick={() => generateForecast()}
            disabled={forecastLoading}
            className="btn-primary"
          >
            {forecastLoading ? 'Generating...' : 'Generate Forecast'}
          </button>
        </div>

        {forecastData && (
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-medium text-blue-900 mb-2">
              {forecastDays}-day {forecastModel} forecast
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-blue-700">Current Price:</span>
                <div className="font-medium">${forecastData.current_price?.toFixed(2)}</div>
              </div>
              <div>
                <span className="text-blue-700">Predicted Price:</span>
                <div className="font-medium">
                  ${forecastData.forecast?.predictions?.slice(-1)[0]?.toFixed(2) || 'N/A'}
                </div>
              </div>
              <div>
                <span className="text-blue-700">Model:</span>
                <div className="font-medium capitalize">{forecastData.forecast?.model}</div>
              </div>
              <div>
                <span className="text-blue-700">Confidence:</span>
                <div className="font-medium">
                  {(forecastData.forecast?.confidence * 100)?.toFixed(0) || 'N/A'}%
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StockDetail;