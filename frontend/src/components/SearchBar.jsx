import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Zap, TrendingUp } from 'lucide-react';
import { useQuery } from 'react-query';
import { stockAPI } from '../services/api';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const searchRef = useRef(null);

  const { data: searchResults, isLoading } = useQuery(
    ['search', query],
    () => stockAPI.search(query),
    {
      enabled: query.length > 1,
      select: (data) => data.data.results,
    }
  );

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelectStock = (symbol) => {
    setQuery('');
    setIsOpen(false);
    navigate(`/stock/${symbol}`);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/stock/${query.toUpperCase()}`);
      setQuery('');
      setIsOpen(false);
    }
  };

  return (
    <div className="relative" ref={searchRef}>
      <form onSubmit={handleSubmit} className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400 dark:text-gray-500" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder="Search stocks (e.g., AAPL, Tesla)"
          className="block w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg leading-5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:focus:border-primary-500 transition-all duration-200"
        />
      </form>

      {/* Search Results Dropdown */}
      {isOpen && query.length > 1 && (
        <div className="absolute z-10 mt-2 w-full bg-white dark:bg-gray-800 shadow-lg max-h-96 rounded-lg py-2 text-base ring-1 ring-black dark:ring-gray-700 ring-opacity-5 overflow-auto focus:outline-none border border-gray-200 dark:border-gray-700">
          {isLoading ? (
            <div className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400 flex items-center gap-2">
              <div className="animate-spin h-4 w-4 border-2 border-primary-500 border-t-transparent rounded-full"></div>
              Searching...
            </div>
          ) : searchResults && searchResults.length > 0 ? (
            <>
              <div className="px-4 py-2 text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide">Results</div>
              {searchResults.map((stock, idx) => (
                <button
                  key={stock.symbol}
                  onClick={() => handleSelectStock(stock.symbol)}
                  className="w-full text-left px-4 py-3 text-sm text-gray-900 dark:text-gray-100 hover:bg-primary-50 dark:hover:bg-gray-700 focus:bg-primary-100 dark:focus:bg-gray-700 cursor-pointer transition-all duration-150 border-b border-gray-100 dark:border-gray-700 last:border-b-0 group"
                >
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded group-hover:scale-110 transition-transform">
                        <TrendingUp className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                      </div>
                      <div>
                        <span className="font-bold text-gray-900 dark:text-white">{stock.symbol}</span>
                        <span className="ml-2 text-gray-600 dark:text-gray-400 text-xs">{stock.name}</span>
                      </div>
                    </div>
                    {stock.price && (
                      <div className="text-right">
                        <span className="font-semibold text-gray-900 dark:text-white">${stock.price.toFixed(2)}</span>
                      </div>
                    )}
                  </div>
                </button>
              ))}
            </>
          ) : query.length > 1 ? (
            <div className="px-4 py-8 text-center">
              <Zap className="h-8 w-8 text-gray-300 dark:text-gray-600 mx-auto mb-2 opacity-50" />
              <p className="text-sm text-gray-500 dark:text-gray-400">No results found</p>
              <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">Press Enter to search for "{query.toUpperCase()}"</p>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
};

export default SearchBar;