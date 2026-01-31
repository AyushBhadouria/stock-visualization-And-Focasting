import React, { useState } from 'react';
import { Search, Filter, TrendingUp, TrendingDown } from 'lucide-react';

export const StockScreener = () => {
  const [symbols, setSymbols] = useState('');
  const [criteria, setCriteria] = useState({
    price_min: null,
    price_max: null,
    market_cap_min: null,
    pe_ratio_max: null,
    min_volume: null,
    rsi_oversold: false,
    rsi_overbought: false,
    sma_crossover: 'both'
  });
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const runScreen = async () => {
    if (!symbols.trim()) return;

    setLoading(true);
    try {
      const symbolList = symbols.split(',').map(s => s.trim().toUpperCase());
      const params = new URLSearchParams();
      
      symbolList.forEach(s => params.append('symbols', s));
      if (criteria.price_min) params.append('price_min', criteria.price_min);
      if (criteria.price_max) params.append('price_max', criteria.price_max);
      if (criteria.market_cap_min) params.append('market_cap_min', criteria.market_cap_min);
      if (criteria.pe_ratio_max) params.append('pe_ratio_max', criteria.pe_ratio_max);
      if (criteria.min_volume) params.append('min_volume', criteria.min_volume);
      if (criteria.rsi_oversold) params.append('rsi_oversold', true);
      if (criteria.rsi_overbought) params.append('rsi_overbought', true);
      if (criteria.sma_crossover !== 'both') params.append('sma_crossover', criteria.sma_crossover);

      const response = await fetch(`/api/screener/screen?${params}`);
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error('Screening error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-900 p-6 rounded-lg">
      <h2 className="text-2xl font-bold text-white mb-6">Stock Screener</h2>

      {/* Input Section */}
      <div className="bg-gray-800 p-6 rounded-lg mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-white mb-2">Stock Symbols (comma-separated)</label>
            <input
              type="text"
              value={symbols}
              onChange={(e) => setSymbols(e.target.value)}
              placeholder="AAPL, MSFT, GOOGL, TSLA"
              className="w-full bg-gray-700 text-white px-4 py-2 rounded border border-gray-600 focus:border-blue-500 outline-none"
            />
          </div>
        </div>

        {/* Criteria */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="block text-white text-sm mb-1">Price Min</label>
            <input
              type="number"
              value={criteria.price_min || ''}
              onChange={(e) => setCriteria({...criteria, price_min: e.target.value ? parseFloat(e.target.value) : null})}
              className="w-full bg-gray-700 text-white px-3 py-2 rounded text-sm border border-gray-600"
              placeholder="0"
            />
          </div>
          <div>
            <label className="block text-white text-sm mb-1">Price Max</label>
            <input
              type="number"
              value={criteria.price_max || ''}
              onChange={(e) => setCriteria({...criteria, price_max: e.target.value ? parseFloat(e.target.value) : null})}
              className="w-full bg-gray-700 text-white px-3 py-2 rounded text-sm border border-gray-600"
              placeholder="999"
            />
          </div>
          <div>
            <label className="block text-white text-sm mb-1">P/E Ratio Max</label>
            <input
              type="number"
              value={criteria.pe_ratio_max || ''}
              onChange={(e) => setCriteria({...criteria, pe_ratio_max: e.target.value ? parseFloat(e.target.value) : null})}
              className="w-full bg-gray-700 text-white px-3 py-2 rounded text-sm border border-gray-600"
              placeholder="25"
            />
          </div>
          <div>
            <label className="block text-white text-sm mb-1">Min Volume</label>
            <input
              type="number"
              value={criteria.min_volume || ''}
              onChange={(e) => setCriteria({...criteria, min_volume: e.target.value ? parseInt(e.target.value) : null})}
              className="w-full bg-gray-700 text-white px-3 py-2 rounded text-sm border border-gray-600"
              placeholder="1000000"
            />
          </div>
        </div>

        {/* Checkboxes */}
        <div className="flex gap-6 mb-4">
          <label className="flex items-center text-white">
            <input
              type="checkbox"
              checked={criteria.rsi_oversold}
              onChange={(e) => setCriteria({...criteria, rsi_oversold: e.target.checked})}
              className="mr-2"
            />
            RSI Oversold (&lt;30)
          </label>
          <label className="flex items-center text-white">
            <input
              type="checkbox"
              checked={criteria.rsi_overbought}
              onChange={(e) => setCriteria({...criteria, rsi_overbought: e.target.checked})}
              className="mr-2"
            />
            RSI Overbought (&gt;70)
          </label>
        </div>

        {/* SMA Crossover */}
        <div className="mb-4">
          <label className="block text-white mb-2">SMA Crossover</label>
          <select
            value={criteria.sma_crossover}
            onChange={(e) => setCriteria({...criteria, sma_crossover: e.target.value})}
            className="bg-gray-700 text-white px-4 py-2 rounded border border-gray-600"
          >
            <option value="both">Any</option>
            <option value="bullish">Bullish (50 &gt; 200)</option>
            <option value="bearish">Bearish (50 &lt; 200)</option>
          </select>
        </div>

        <button
          onClick={runScreen}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded"
        >
          {loading ? 'Screening...' : 'Run Screen'}
        </button>
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-white">
            <thead className="bg-gray-800">
              <tr>
                <th className="px-4 py-3 text-left">Symbol</th>
                <th className="px-4 py-3 text-right">Price</th>
                <th className="px-4 py-3 text-right">Market Cap</th>
                <th className="px-4 py-3 text-right">P/E Ratio</th>
                <th className="px-4 py-3 text-right">Volume</th>
                <th className="px-4 py-3 text-right">RSI</th>
                <th className="px-4 py-3 text-center">Trend</th>
              </tr>
            </thead>
            <tbody>
              {results.map((stock, idx) => (
                <tr key={idx} className="border-t border-gray-700 hover:bg-gray-800">
                  <td className="px-4 py-3 font-semibold">{stock.symbol}</td>
                  <td className="px-4 py-3 text-right">${stock.price?.toFixed(2) || 'N/A'}</td>
                  <td className="px-4 py-3 text-right">
                    ${stock.marketCap ? (stock.marketCap / 1e9).toFixed(1) + 'B' : 'N/A'}
                  </td>
                  <td className="px-4 py-3 text-right">{stock.pe_ratio?.toFixed(2) || 'N/A'}</td>
                  <td className="px-4 py-3 text-right">
                    {stock.volume ? (stock.volume / 1e6).toFixed(1) + 'M' : 'N/A'}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <span className={stock.rsi > 70 ? 'text-red-500' : stock.rsi < 30 ? 'text-green-500' : 'text-white'}>
                      {stock.rsi?.toFixed(1) || 'N/A'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    {stock.sma_50 && stock.sma_200 ? (
                      stock.sma_50 > stock.sma_200 ? (
                        <TrendingUp className="inline text-green-500" size={18} />
                      ) : (
                        <TrendingDown className="inline text-red-500" size={18} />
                      )
                    ) : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {!loading && results.length === 0 && symbols && (
        <div className="text-center text-gray-400 py-8">
          No stocks matched your criteria
        </div>
      )}
    </div>
  );
};

export default StockScreener;
