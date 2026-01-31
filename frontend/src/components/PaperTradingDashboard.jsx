import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown } from 'lucide-react';

export const PaperTradingDashboard = () => {
  const [portfolio, setPortfolio] = useState({
    cash: 100000,
    stocks_value: 0,
    total_value: 100000,
    return: 0,
    return_percent: 0
  });
  
  const [positions, setPositions] = useState([]);
  const [trades, setTrades] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [tradeForm, setTradeForm] = useState({
    symbol: '',
    quantity: '',
    price: ''
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    try {
      const [portfolioRes, positionsRes, tradeRes, metricsRes] = await Promise.all([
        fetch('/api/paper-trading/portfolio-value'),
        fetch('/api/paper-trading/positions'),
        fetch('/api/paper-trading/trade-history'),
        fetch('/api/paper-trading/performance')
      ]);

      if (portfolioRes.ok) setPortfolio(await portfolioRes.json());
      if (positionsRes.ok) {
        const data = await positionsRes.json();
        setPositions(data.positions || []);
      }
      if (tradeRes.ok) {
        const data = await tradeRes.json();
        setTrades(data.trades || []);
      }
      if (metricsRes.ok) {
        const data = await metricsRes.json();
        setMetrics(data.metrics);
      }
    } catch (error) {
      console.error('Error fetching portfolio data:', error);
    }
  };

  const handleTrade = async (type) => {
    if (!tradeForm.symbol || !tradeForm.quantity || !tradeForm.price) return;

    setLoading(true);
    try {
      const endpoint = `/api/paper-trading/${type}`;
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: tradeForm.symbol.toUpperCase(),
          quantity: parseInt(tradeForm.quantity),
          price: parseFloat(tradeForm.price)
        })
      });

      if (response.ok) {
        setTradeForm({ symbol: '', quantity: '', price: '' });
        fetchPortfolioData();
      }
    } catch (error) {
      console.error('Trade error:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetAccount = async () => {
    if (window.confirm('Reset account to $100,000?')) {
      try {
        await fetch('/api/paper-trading/reset?initial_cash=100000', { method: 'POST' });
        fetchPortfolioData();
      } catch (error) {
        console.error('Reset error:', error);
      }
    }
  };

  return (
    <div className="bg-gray-900 p-6 rounded-lg">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-white">Paper Trading Dashboard</h2>
        <button
          onClick={resetAccount}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
        >
          Reset Account
        </button>
      </div>

      {/* Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded">
          <p className="text-gray-400 text-sm">Cash</p>
          <p className="text-white text-2xl font-bold">${portfolio.cash?.toFixed(0) || 0}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded">
          <p className="text-gray-400 text-sm">Stocks Value</p>
          <p className="text-white text-2xl font-bold">${portfolio.stocks_value?.toFixed(0) || 0}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded">
          <p className="text-gray-400 text-sm">Total Value</p>
          <p className="text-white text-2xl font-bold">${portfolio.total_value?.toFixed(0) || 0}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded">
          <p className="text-gray-400 text-sm">Return</p>
          <p className={`text-2xl font-bold ${portfolio.return_percent >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            {portfolio.return_percent?.toFixed(2)}%
          </p>
        </div>
      </div>

      {/* Trade Form */}
      <div className="bg-gray-800 p-6 rounded-lg mb-6">
        <h3 className="text-lg font-semibold text-white mb-4">Place Trade</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Symbol (e.g., AAPL)"
            value={tradeForm.symbol}
            onChange={(e) => setTradeForm({...tradeForm, symbol: e.target.value})}
            className="bg-gray-700 text-white px-4 py-2 rounded border border-gray-600 focus:border-blue-500 outline-none"
          />
          <input
            type="number"
            placeholder="Quantity"
            value={tradeForm.quantity}
            onChange={(e) => setTradeForm({...tradeForm, quantity: e.target.value})}
            className="bg-gray-700 text-white px-4 py-2 rounded border border-gray-600 focus:border-blue-500 outline-none"
          />
          <input
            type="number"
            placeholder="Price"
            value={tradeForm.price}
            onChange={(e) => setTradeForm({...tradeForm, price: e.target.value})}
            className="bg-gray-700 text-white px-4 py-2 rounded border border-gray-600 focus:border-blue-500 outline-none"
          />
          <div className="flex gap-2">
            <button
              onClick={() => handleTrade('buy')}
              disabled={loading}
              className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded"
            >
              Buy
            </button>
            <button
              onClick={() => handleTrade('sell')}
              disabled={loading}
              className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded"
            >
              Sell
            </button>
          </div>
        </div>
      </div>

      {/* Positions */}
      {positions.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">Open Positions</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-white">
              <thead className="bg-gray-800">
                <tr>
                  <th className="px-4 py-3 text-left">Symbol</th>
                  <th className="px-4 py-3 text-right">Qty</th>
                  <th className="px-4 py-3 text-right">Avg Price</th>
                  <th className="px-4 py-3 text-right">Current Price</th>
                  <th className="px-4 py-3 text-right">Value</th>
                  <th className="px-4 py-3 text-right">Unrealized P&L</th>
                </tr>
              </thead>
              <tbody>
                {positions.map((pos, idx) => (
                  <tr key={idx} className="border-t border-gray-700 hover:bg-gray-800">
                    <td className="px-4 py-3 font-semibold">{pos.symbol}</td>
                    <td className="px-4 py-3 text-right">{pos.quantity}</td>
                    <td className="px-4 py-3 text-right">${pos.avg_price.toFixed(2)}</td>
                    <td className="px-4 py-3 text-right">${pos.current_price.toFixed(2)}</td>
                    <td className="px-4 py-3 text-right">${pos.value.toFixed(2)}</td>
                    <td className={`px-4 py-3 text-right font-semibold ${pos.unrealized_pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                      ${pos.unrealized_pnl.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Performance Metrics */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400 text-sm">Total Trades</p>
            <p className="text-white text-2xl font-bold">{metrics.total_trades}</p>
          </div>
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400 text-sm">Win Rate</p>
            <p className="text-white text-2xl font-bold">{metrics.win_rate?.toFixed(1)}%</p>
          </div>
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400 text-sm">Max Drawdown</p>
            <p className="text-white text-2xl font-bold">{metrics.max_drawdown?.toFixed(2)}%</p>
          </div>
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400 text-sm">Total P&L</p>
            <p className={`text-2xl font-bold ${metrics.total_pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
              ${metrics.total_pnl?.toFixed(2) || 0}
            </p>
          </div>
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400 text-sm">Profit Factor</p>
            <p className="text-white text-2xl font-bold">{metrics.profit_factor?.toFixed(2)}</p>
          </div>
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400 text-sm">Avg Win / Loss</p>
            <p className="text-white text-sm">
              ${metrics.avg_win?.toFixed(0) || 0} / ${metrics.avg_loss?.toFixed(0) || 0}
            </p>
          </div>
        </div>
      )}

      {/* Trade History */}
      {trades.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Trade History</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-white text-sm">
              <thead className="bg-gray-800">
                <tr>
                  <th className="px-4 py-3 text-left">Symbol</th>
                  <th className="px-4 py-3 text-right">Qty</th>
                  <th className="px-4 py-3 text-right">Buy Price</th>
                  <th className="px-4 py-3 text-right">Sell Price</th>
                  <th className="px-4 py-3 text-right">P&L</th>
                  <th className="px-4 py-3 text-right">Return %</th>
                </tr>
              </thead>
              <tbody>
                {trades.slice(-10).reverse().map((trade, idx) => (
                  <tr key={idx} className="border-t border-gray-700 hover:bg-gray-800">
                    <td className="px-4 py-3 font-semibold">{trade.symbol}</td>
                    <td className="px-4 py-3 text-right">{trade.quantity}</td>
                    <td className="px-4 py-3 text-right">${trade.buy_price.toFixed(2)}</td>
                    <td className="px-4 py-3 text-right">${trade.sell_price.toFixed(2)}</td>
                    <td className={`px-4 py-3 text-right font-semibold ${trade.pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                      ${trade.pnl.toFixed(2)}
                    </td>
                    <td className={`px-4 py-3 text-right font-semibold ${trade.pnl_percent >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                      {trade.pnl_percent.toFixed(2)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default PaperTradingDashboard;
