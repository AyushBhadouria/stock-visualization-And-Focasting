import React from 'react';
import PaperTradingDashboard from '../components/PaperTradingDashboard';

export const PaperTrading = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Paper Trading</h1>
        <p className="text-gray-400">Simulate trading with virtual money to test your strategies</p>
      </div>
      <PaperTradingDashboard />
    </div>
  );
};

export default PaperTrading;
