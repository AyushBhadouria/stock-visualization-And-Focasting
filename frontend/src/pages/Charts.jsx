import React from 'react';
import AdvancedChart from '../components/AdvancedChart';

export const Charts = () => {
  const [symbol, setSymbol] = React.useState('AAPL');

  return (
    <div className="space-y-6">
      <div className="flex gap-4">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          placeholder="Enter stock symbol"
          className="flex-1 bg-gray-800 text-white px-4 py-2 rounded border border-gray-700 focus:border-blue-500 outline-none"
        />
      </div>

      <AdvancedChart symbol={symbol} />
    </div>
  );
};

export default Charts;
