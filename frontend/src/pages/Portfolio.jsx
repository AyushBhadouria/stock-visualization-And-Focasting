import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Plus, TrendingUp, TrendingDown, DollarSign } from 'lucide-react';
import { portfolioAPI } from '../services/api';

const Portfolio = () => {
  const [showAddTransaction, setShowAddTransaction] = useState(false);
  const [transactionForm, setTransactionForm] = useState({
    symbol: '',
    transaction_type: 'buy',
    quantity: '',
    price: '',
    transaction_date: new Date().toISOString().split('T')[0]
  });

  const queryClient = useQueryClient();

  const { data: portfolioData, isLoading } = useQuery(
    'portfolio',
    portfolioAPI.getPortfolio,
    {
      select: (data) => data.data,
    }
  );

  const { data: transactionsData } = useQuery(
    'transactions',
    portfolioAPI.getTransactions,
    {
      select: (data) => data.data.transactions,
    }
  );

  const addTransactionMutation = useMutation(
    portfolioAPI.addTransaction,
    {
      onSuccess: () => {
        queryClient.invalidateQueries('portfolio');
        queryClient.invalidateQueries('transactions');
        setShowAddTransaction(false);
        setTransactionForm({
          symbol: '',
          transaction_type: 'buy',
          quantity: '',
          price: '',
          transaction_date: new Date().toISOString().split('T')[0]
        });
      },
    }
  );

  const handleSubmitTransaction = (e) => {
    e.preventDefault();
    addTransactionMutation.mutate({
      ...transactionForm,
      quantity: parseFloat(transactionForm.quantity),
      price: parseFloat(transactionForm.price),
      transaction_date: new Date(transactionForm.transaction_date).toISOString()
    });
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg">Loading portfolio...</div>
      </div>
    );
  }

  const portfolio = portfolioData || {};
  const isPositive = (portfolio.total_gain_loss || 0) >= 0;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Portfolio</h1>
          <p className="text-gray-600">Track your investments</p>
        </div>
        <button
          onClick={() => setShowAddTransaction(true)}
          className="btn-primary flex items-center"
        >
          <Plus size={20} className="mr-2" />
          Add Transaction
        </button>
      </div>

      {/* Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Value</p>
              <p className="text-2xl font-bold text-gray-900">
                ${portfolio.total_value?.toFixed(2) || '0.00'}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-gray-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-gray-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Cost</p>
              <p className="text-2xl font-bold text-gray-900">
                ${portfolio.total_cost?.toFixed(2) || '0.00'}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className={`p-2 rounded-lg ${isPositive ? 'bg-green-100' : 'bg-red-100'}`}>
              {isPositive ? 
                <TrendingUp className="h-6 w-6 text-green-600" /> : 
                <TrendingDown className="h-6 w-6 text-red-600" />
              }
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Gain/Loss</p>
              <p className={`text-2xl font-bold ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                {isPositive ? '+' : ''}${portfolio.total_gain_loss?.toFixed(2) || '0.00'}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className={`p-2 rounded-lg ${isPositive ? 'bg-green-100' : 'bg-red-100'}`}>
              {isPositive ? 
                <TrendingUp className="h-6 w-6 text-green-600" /> : 
                <TrendingDown className="h-6 w-6 text-red-600" />
              }
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Return %</p>
              <p className={`text-2xl font-bold ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                {isPositive ? '+' : ''}{portfolio.total_gain_loss_percent?.toFixed(2) || '0.00'}%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Holdings */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Holdings</h2>
        {portfolio.holdings && portfolio.holdings.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Symbol</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Avg Cost</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Current Price</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Market Value</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gain/Loss</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {portfolio.holdings.map((holding) => {
                  const isHoldingPositive = holding.gain_loss >= 0;
                  return (
                    <tr key={holding.symbol} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap font-medium text-primary-600">
                        {holding.symbol}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {holding.quantity}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ${holding.avg_cost.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ${holding.current_price.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ${holding.current_value.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <div className={isHoldingPositive ? 'text-green-600' : 'text-red-600'}>
                          <div>{isHoldingPositive ? '+' : ''}${holding.gain_loss.toFixed(2)}</div>
                          <div className="text-xs">
                            ({isHoldingPositive ? '+' : ''}{holding.gain_loss_percent.toFixed(2)}%)
                          </div>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <p>No holdings yet. Add your first transaction to get started.</p>
          </div>
        )}
      </div>

      {/* Add Transaction Modal */}
      {showAddTransaction && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Add Transaction</h3>
            <form onSubmit={handleSubmitTransaction} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Symbol</label>
                <input
                  type="text"
                  value={transactionForm.symbol}
                  onChange={(e) => setTransactionForm({...transactionForm, symbol: e.target.value.toUpperCase()})}
                  className="input mt-1"
                  placeholder="AAPL"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Type</label>
                <select
                  value={transactionForm.transaction_type}
                  onChange={(e) => setTransactionForm({...transactionForm, transaction_type: e.target.value})}
                  className="input mt-1"
                >
                  <option value="buy">Buy</option>
                  <option value="sell">Sell</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Quantity</label>
                <input
                  type="number"
                  step="0.01"
                  value={transactionForm.quantity}
                  onChange={(e) => setTransactionForm({...transactionForm, quantity: e.target.value})}
                  className="input mt-1"
                  placeholder="10"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Price</label>
                <input
                  type="number"
                  step="0.01"
                  value={transactionForm.price}
                  onChange={(e) => setTransactionForm({...transactionForm, price: e.target.value})}
                  className="input mt-1"
                  placeholder="150.00"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Date</label>
                <input
                  type="date"
                  value={transactionForm.transaction_date}
                  onChange={(e) => setTransactionForm({...transactionForm, transaction_date: e.target.value})}
                  className="input mt-1"
                  required
                />
              </div>
              
              <div className="flex space-x-3 pt-4">
                <button
                  type="submit"
                  disabled={addTransactionMutation.isLoading}
                  className="btn-primary flex-1"
                >
                  {addTransactionMutation.isLoading ? 'Adding...' : 'Add Transaction'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowAddTransaction(false)}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Portfolio;