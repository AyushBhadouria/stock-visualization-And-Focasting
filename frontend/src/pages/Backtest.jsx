import React from 'react';
import BacktestingEngine from '../components/BacktestingEngine';

export const Backtest = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Backtesting Engine</h1>
        <p className="text-gray-400">Test your trading strategies on historical data</p>
      </div>
      <BacktestingEngine />
    </div>
  );
};

export default Backtest;
