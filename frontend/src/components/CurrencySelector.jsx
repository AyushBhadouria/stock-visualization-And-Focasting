import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import useCurrencyStore from '../hooks/useCurrency';

const CurrencySelector = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { selectedCurrency, currencies, setCurrency } = useCurrencyStore();

  const handleCurrencyChange = (currency) => {
    setCurrency(currency);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-3 py-2 text-sm bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
      >
        <span>{currencies[selectedCurrency]?.symbol}</span>
        <span>{selectedCurrency}</span>
        <ChevronDown size={16} className={`transform transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg z-50">
          <div className="py-1">
            {Object.entries(currencies).map(([code, info]) => (
              <button
                key={code}
                onClick={() => handleCurrencyChange(code)}
                className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 flex items-center justify-between ${
                  selectedCurrency === code ? 'bg-primary-50 dark:bg-primary-900/40 text-primary-600 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span>{info.symbol}</span>
                  <span>{code}</span>
                </div>
                <span className="text-xs text-gray-500 dark:text-gray-400">{info.name}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CurrencySelector;