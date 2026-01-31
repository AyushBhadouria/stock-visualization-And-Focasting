import React, { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart } from 'recharts';
import { AlertCircle, Loader } from 'lucide-react';

export const AdvancedChart = ({ symbol, initialChartType = 'line' }) => {
  const [data, setData] = useState([]);
  const [chartType, setChartType] = useState(initialChartType);
  const [period, setPeriod] = useState('1mo');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [indicators, setIndicators] = useState([]);

  useEffect(() => {
    fetchChartData();
  }, [symbol, period]);

  const fetchChartData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `/api/charting/candlesticks/${symbol}?period=${period}`
      );
      
      if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.status}`);
      }
      
      const result = await response.json();
      
      // Format data for chart display
      if (result.data && Array.isArray(result.data)) {
        const formattedData = result.data.map((candle, idx) => ({
          ...candle,
          index: idx,
          date: new Date(candle.time * 1000).toLocaleDateString()
        }));
        setData(formattedData);
      } else {
        setError('No data returned from API');
        setData([]);
      }
    } catch (error) {
      console.error('Error fetching chart data:', error);
      setError(error.message || 'Failed to fetch chart data');
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  const addIndicator = async (indicatorType) => {
    try {
      const endpoint = `/api/indicators/${indicatorType}/${symbol}`;
      const response = await fetch(endpoint);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch ${indicatorType}`);
      }
      
      const result = await response.json();
      
      setIndicators([...indicators, {
        type: indicatorType,
        data: result.data
      }]);
    } catch (error) {
      console.error(`Error adding ${indicatorType}:`, error);
    }
  };

  const removeIndicator = (index) => {
    setIndicators(indicators.filter((_, i) => i !== index));
  };

  return (
    <div className="bg-gray-900 p-6 rounded-lg space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-white">{symbol}</h2>
          <p className="text-gray-400 text-sm">{period.toUpperCase()} • {data.length} candles</p>
        </div>
        
        <div className="flex gap-4">
          {/* Chart Type Selector */}
          <select
            value={chartType}
            onChange={(e) => setChartType(e.target.value)}
            className="bg-gray-800 text-white px-3 py-2 rounded border border-gray-700 hover:border-gray-500 focus:outline-none"
          >
            <option value="line">Line Chart</option>
            <option value="area">Area Chart</option>
            <option value="candlestick">Candlestick</option>
          </select>

          {/* Period Selector */}
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="bg-gray-800 text-white px-3 py-2 rounded border border-gray-700 hover:border-gray-500 focus:outline-none"
          >
            <option value="1d">1 Day</option>
            <option value="5d">5 Days</option>
            <option value="1mo">1 Month</option>
            <option value="3mo">3 Months</option>
            <option value="6mo">6 Months</option>
            <option value="1y">1 Year</option>
          </select>
        </div>
      </div>

      {/* Chart Area */}
      {loading ? (
        <div className="h-96 flex items-center justify-center bg-gray-800 rounded">
          <div className="text-center">
            <Loader className="mx-auto mb-2 text-blue-500 animate-spin" size={32} />
            <p className="text-gray-400">Loading chart data...</p>
          </div>
        </div>
      ) : error ? (
        <div className="h-96 flex items-center justify-center bg-gray-800 rounded">
          <div className="text-center">
            <AlertCircle className="mx-auto mb-2 text-red-500" size={32} />
            <p className="text-red-400">{error}</p>
            <p className="text-gray-400 text-sm mt-2">Check if symbol exists and try again</p>
          </div>
        </div>
      ) : data.length === 0 ? (
        <div className="h-96 flex items-center justify-center bg-gray-800 rounded">
          <div className="text-center">
            <AlertCircle className="mx-auto mb-2 text-yellow-500" size={32} />
            <p className="text-yellow-400">No data available</p>
            <p className="text-gray-400 text-sm mt-2">Try a different symbol or period</p>
          </div>
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          {chartType === 'line' ? (
            <LineChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis 
                dataKey="date" 
                stroke="#888"
                tick={{ fontSize: 12 }}
              />
              <YAxis stroke="#888" tick={{ fontSize: 12 }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: '1px solid #444',
                  borderRadius: '8px'
                }}
                labelStyle={{ color: '#fff' }}
                formatter={(value) => value ? value.toFixed(2) : 'N/A'}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="close" 
                stroke="#3b82f6" 
                name="Close Price"
                dot={false}
                strokeWidth={2}
              />
              <Line 
                type="monotone" 
                dataKey="open" 
                stroke="#10b981" 
                name="Open Price"
                dot={false}
                strokeWidth={1}
                opacity={0.6}
              />
            </LineChart>
          ) : chartType === 'area' ? (
            <AreaChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis 
                dataKey="date" 
                stroke="#888"
                tick={{ fontSize: 12 }}
              />
              <YAxis stroke="#888" tick={{ fontSize: 12 }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: '1px solid #444',
                  borderRadius: '8px'
                }}
                labelStyle={{ color: '#fff' }}
                formatter={(value) => value ? value.toFixed(2) : 'N/A'}
              />
              <Legend />
              <Area 
                type="monotone" 
                dataKey="close" 
                fill="#3b82f6" 
                stroke="#1e40af"
                name="Close Price"
                opacity={0.7}
              />
            </AreaChart>
          ) : (
            <ComposedChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis 
                dataKey="date" 
                stroke="#888"
                tick={{ fontSize: 12 }}
              />
              <YAxis stroke="#888" tick={{ fontSize: 12 }} />
              <YAxis yAxisId="right" orientation="right" stroke="#888" tick={{ fontSize: 12 }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: '1px solid #444',
                  borderRadius: '8px'
                }}
                labelStyle={{ color: '#fff' }}
                formatter={(value) => value ? value.toFixed(2) : 'N/A'}
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-gray-800 p-3 rounded border border-gray-600">
                        <p className="text-gray-300 text-sm">{data.date}</p>
                        <p className="text-green-400 text-sm">O: ${data.open?.toFixed(2)}</p>
                        <p className="text-blue-400 text-sm">H: ${data.high?.toFixed(2)}</p>
                        <p className="text-red-400 text-sm">L: ${data.low?.toFixed(2)}</p>
                        <p className="text-white text-sm font-bold">C: ${data.close?.toFixed(2)}</p>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Legend />
              <Bar dataKey="volume" fill="#6366f1" opacity={0.3} yAxisId="right" name="Volume" />
              <Line 
                type="monotone" 
                dataKey="close" 
                stroke="#3b82f6" 
                name="Close"
                dot={false}
                strokeWidth={2}
              />
            </ComposedChart>
          )}
        </ResponsiveContainer>
      )}

      {/* Indicators Section */}
      <div className="border-t border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-white mb-4">Technical Indicators</h3>
        
        <div className="flex flex-wrap gap-2 mb-6">
          <button
            onClick={() => addIndicator('macd')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded text-sm transition"
          >
            + MACD
          </button>
          <button
            onClick={() => addIndicator('bollinger-bands')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded text-sm transition"
          >
            + Bollinger Bands
          </button>
          <button
            onClick={() => addIndicator('rsi')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded text-sm transition"
          >
            + RSI
          </button>
          <button
            onClick={() => addIndicator('stochastic')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded text-sm transition"
          >
            + Stochastic
          </button>
          <button
            onClick={() => addIndicator('atr')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded text-sm transition"
          >
            + ATR
          </button>
        </div>

        {indicators.length > 0 && (
          <div className="space-y-4">
            {indicators.map((indicator, index) => (
              <div
                key={index}
                className="bg-gray-800 p-4 rounded relative"
              >
                <button
                  onClick={() => removeIndicator(index)}
                  className="absolute top-2 right-2 text-red-500 hover:text-red-400 font-bold"
                >
                  ✕
                </button>
                <h4 className="text-white font-semibold mb-2">{indicator.type.toUpperCase()}</h4>
                <p className="text-gray-400 text-sm">Indicator data loaded</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdvancedChart;
