import { create } from 'zustand';

const useCurrencyStore = create((set, get) => ({
  selectedCurrency: 'USD',
  currencies: {
    'USD': { name: 'US Dollar', symbol: '$' },
    'INR': { name: 'Indian Rupee', symbol: '₹' },
    'CNY': { name: 'Chinese Yuan', symbol: '¥' },
    'AED': { name: 'UAE Dirham', symbol: 'د.إ' },
    'EUR': { name: 'Euro', symbol: '€' },
    'GBP': { name: 'British Pound', symbol: '£' },
    'JPY': { name: 'Japanese Yen', symbol: '¥' },
  },
  exchangeRates: {
    'USD': 1.0,
    'INR': 83.12,
    'CNY': 7.24,
    'AED': 3.67,
    'EUR': 0.92,
    'GBP': 0.79,
    'JPY': 149.50,
  },

  setCurrency: (currency) => {
    set({ selectedCurrency: currency });
    localStorage.setItem('selectedCurrency', currency);
  },

  convertPrice: (usdPrice, targetCurrency = null) => {
    const currency = targetCurrency || get().selectedCurrency;
    const rate = get().exchangeRates[currency] || 1.0;
    return usdPrice * rate;
  },

  formatPrice: (usdPrice, targetCurrency = null) => {
    const currency = targetCurrency || get().selectedCurrency;
    const convertedPrice = get().convertPrice(usdPrice, currency);
    const symbol = get().currencies[currency]?.symbol || '$';
    
    return `${symbol}${convertedPrice.toFixed(2)}`;
  },

  initializeCurrency: () => {
    const savedCurrency = localStorage.getItem('selectedCurrency');
    if (savedCurrency && get().currencies[savedCurrency]) {
      set({ selectedCurrency: savedCurrency });
    }
  },
}));

export default useCurrencyStore;