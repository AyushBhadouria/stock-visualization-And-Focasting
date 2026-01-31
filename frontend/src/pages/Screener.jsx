import React from 'react';
import StockScreener from '../components/StockScreener';

export const Screener = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">Stock Screener</h1>
      <p className="text-gray-400">Filter and scan stocks based on multiple technical and fundamental criteria</p>
      <StockScreener />
    </div>
  );
};

export default Screener;
