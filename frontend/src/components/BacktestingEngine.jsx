import React, { useState } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown } from 'lucide-react';

export const BacktestingEngine = () => {
  const [backtest, setBacktest] = useState({
    symbol: 'AAPL',
    start_date: '2023-01-01',
    end_date: '2024-01-01',
    strategy: 'rsi',
    initial_capital: 100000
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [comparing, setComparing] = useState(false);
  const [comparison, setComparison] = useState(null);

  const runBacktest = async () => {
    setLoading(true);
    try {
      let endpoint = `/api/backtest/${backtest.strategy}-strategy/${backtest.symbol}`;
      const params = new URLSearchParams({
        start_date: backtest.start_date,
        end_date: backtest.end_date,
        initial_capital: backtest.initial_capital
      });

      if (backtest.strategy === 'rsi') {
        params.append('rsi_oversold', 30);
        params.append('rsi_overbought', 70);
      } else if (backtest.strategy === 'sma_crossover') {
        params.append('fast_period', 50);
        params.append('slow_period', 200);
      }

      const response = await fetch(`${endpoint}?${params}`);
      const data = await response.json();
      setResult(data.result);
      setComparison(null);
    } catch (error) {
      console.error('Backtest error:', error);
    } finally {
      setLoading(false);
    }
  };

  const compareStrategies = async () => {
    setComparing(true);
    try {
      const params = new URLSearchParams({
        start_date: backtest.start_date,
        end_date: backtest.end_date
      });

      const response = await fetch(`/api/backtest/compare-strategies/${backtest.symbol}?${params}`);
      const data = await response.json();
      setComparison(data.strategies);
      setResult(null);
    } catch (error) {
      console.error('Comparison error:', error);
    } finally {
      setComparing(false);
    }
  };

  return (
    <div className="bg-gray-900 p-6 rounded-lg">
      <h2 className="text-3xl font-bold text-white mb-6">Backtesting Engine</h2>

      {/* Input Section */}
      <div className="bg-gray-800 p-6 rounded-lg mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-white mb-2">Stock Symbol</label>
            <input
              type="text"
              value={backtest.symbol}
              onChange={(e) => setBacktest({...backtest, symbol: e.target.value.toUpperCase()})}
              className="w-full bg-gray-700 text-white px-4 py-2 rounded border border-gray-600"
            />
          </div>
          <div>
            <label className="block text-white mb-2">Strategy</label>
            <select
              value={backtest.strategy}
              onChange={(e) => setBacktest({...backtest, strategy: e.target.value})}
              className="w-full bg-gray-700 text-white px-4 py-2 rounded border border-gray-600"
            >
              <option value="rsi">RSI Strategy</option>
              <option value="sma_crossover">SMA Crossover</option>
            </select>
          </div>
          <div>
            <label className="block text-white mb-2">Start Date</label>
            <input
              type="date"
              value={backtest.start_date}
              onChange={(e) => setBacktest({...backtest, start_date: e.target.value})}
              className="w-full bg-gray-700 text-white px-4 py-2 rounded border border-gray-600"
            />
          </div>
          <div>
            <label className="block text-white mb-2">End Date</label>
            <input
              type="date"
              value={backtest.end_date}
              onChange={(e) => setBacktest({...backtest, end_date: e.target.value})}
              className="w-full bg-gray-700 text-white px-4 py-2 rounded border border-gray-600"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
          <button
            onClick={runBacktest}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded"
          >
            {loading ? 'Running...' : 'Run Backtest'}
          </button>
          <button
            onClick={compareStrategies}
            disabled={comparing}
            className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded"
          >
            {comparing ? 'Comparing...' : 'Compare Strategies'}
          </button>
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Metrics */}
          <div className="bg-gray-800 p-6 rounded-lg">
            <h3 className="text-xl font-semibold text-white mb-4">Performance Metrics</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-gray-400 text-sm">Total Trades</p>
                <p className="text-white text-2xl font-bold">{result.metrics.total_trades}</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Win Rate</p>
                <p className="text-white text-2xl font-bold">{result.metrics.win_rate?.toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Total Return</p>
                <p className={`text-2xl font-bold ${result.metrics.total_return_percent >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  {result.metrics.total_return_percent?.toFixed(2)}%
                </p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Max Drawdown</p>
                <p className="text-white text-2xl font-bold">{result.metrics.max_drawdown?.toFixed(2)}%</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Profit Factor</p>
                <p className="text-white text-2xl font-bold">{result.metrics.profit_factor?.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Sharpe Ratio</p>
                <p className="text-white text-2xl font-bold">{result.metrics.sharpe_ratio?.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Gross Profit</p>
                <p className="text-green-500 text-2xl font-bold">${result.metrics.gross_profit?.toFixed(0)}</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Gross Loss</p>
                <p className="text-red-500 text-2xl font-bold">${result.metrics.gross_loss?.toFixed(0)}</p>
              </div>
            </div>
          </div>

          {/* Equity Curve */}
          {result.equity_curve && result.equity_curve.length > 0 && (
            <div className="bg-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-4">Equity Curve</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  data={result.equity_curve.map((val, idx) => ({
                    date: idx,
                    profit: val
                  }))}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                  <Line
                    type="monotone"
                    dataKey="profit"
                    stroke="#10b981"
                    dot={false}
                    name="Equity"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Portfolio Value */}
          {result.portfolio_values && result.portfolio_values.length > 0 && (
            <div className="bg-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-4">Portfolio Value</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  data={result.portfolio_values.map((val, idx) => ({
                    date: idx,
                    value: val
                  }))}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#3b82f6"
                    dot={false}
                    name="Value"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Trades Table */}
          {result.trades && result.trades.length > 0 && (
            <div className="bg-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-4">Trades ({result.trades.length})</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-white text-sm">
                  <thead className="bg-gray-700">
                    <tr>
                      <th className="px-4 py-3 text-left">Entry Price</th>
                      <th className="px-4 py-3 text-left">Exit Price</th>
                      <th className="px-4 py-3 text-right">Qty</th>
                      <th className="px-4 py-3 text-right">P&L</th>
                      <th className="px-4 py-3 text-right">Return %</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.trades.slice(-20).map((trade, idx) => (
                      <tr key={idx} className="border-t border-gray-700">
                        <td className="px-4 py-3">${trade.entry_price.toFixed(2)}</td>
                        <td className="px-4 py-3">${trade.exit_price.toFixed(2)}</td>
                        <td className="px-4 py-3 text-right">{trade.quantity}</td>
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
      )}

      {/* Strategy Comparison */}
      {comparison && (
        <div className="bg-gray-800 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-white mb-4">Strategy Comparison</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border-r border-gray-700 pr-6">
              <h4 className="text-lg text-white font-semibold mb-4">RSI Strategy</h4>
              <div className="space-y-2">
                <p className="text-gray-400">Total Trades: <span className="text-white font-bold">{comparison.rsi.trades}</span></p>
                <p className="text-gray-400">Win Rate: <span className="text-white font-bold">{comparison.rsi.metrics.win_rate?.toFixed(1)}%</span></p>
                <p className="text-gray-400">Total Return: <span className={`font-bold ${comparison.rsi.metrics.total_return_percent >= 0 ? 'text-green-500' : 'text-red-500'}`}>{comparison.rsi.metrics.total_return_percent?.toFixed(2)}%</span></p>
                <p className="text-gray-400">Sharpe Ratio: <span className="text-white font-bold">{comparison.rsi.metrics.sharpe_ratio?.toFixed(2)}</span></p>
              </div>
            </div>
            <div>
              <h4 className="text-lg text-white font-semibold mb-4">SMA Crossover</h4>
              <div className="space-y-2">
                <p className="text-gray-400">Total Trades: <span className="text-white font-bold">{comparison.sma_crossover.trades}</span></p>
                <p className="text-gray-400">Win Rate: <span className="text-white font-bold">{comparison.sma_crossover.metrics.win_rate?.toFixed(1)}%</span></p>
                <p className="text-gray-400">Total Return: <span className={`font-bold ${comparison.sma_crossover.metrics.total_return_percent >= 0 ? 'text-green-500' : 'text-red-500'}`}>{comparison.sma_crossover.metrics.total_return_percent?.toFixed(2)}%</span></p>
                <p className="text-gray-400">Sharpe Ratio: <span className="text-white font-bold">{comparison.sma_crossover.metrics.sharpe_ratio?.toFixed(2)}</span></p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BacktestingEngine;
