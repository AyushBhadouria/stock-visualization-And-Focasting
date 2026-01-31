# Stock Platform - Advanced Features Guide

This document outlines all the new advanced features added to your stock platform.

## 🎯 Table of Contents

1. [Advanced Charting](#advanced-charting)
2. [Technical Indicators](#technical-indicators)
3. [Stock Screener](#stock-screener)
4. [Paper Trading](#paper-trading)
5. [Backtesting Engine](#backtesting-engine)
6. [API Endpoints](#api-endpoints)
7. [Frontend Pages](#frontend-pages)

---

## Advanced Charting

### Features
- **Multiple Chart Types**
  - Candlestick charts
  - Line charts
  - Area charts
  - Heikin Ashi charts

- **Drawing Tools**
  - Fibonacci retracement levels
  - Support & resistance identification
  - Pivot points (daily, weekly, monthly)
  - Donchian channels

- **Multi-Stock Comparison**
  - Compare up to 5 stocks on the same chart
  - Normalized percentage returns for easy comparison

### Usage
```
Navigate to /charts
1. Enter stock symbol (e.g., AAPL)
2. Select chart type from dropdown
3. Choose time period (1D, 1W, 1M, 3M, 6M, 1Y)
4. Add indicators as needed
```

### API Endpoints
```
GET /api/charting/candlesticks/{symbol}?period=1mo
GET /api/charting/heikin-ashi/{symbol}?period=1mo
POST /api/charting/compare?symbols=AAPL&symbols=MSFT
GET /api/charting/fibonacci/{symbol}?period=1mo
GET /api/charting/pivot-points/{symbol}
GET /api/charting/support-resistance/{symbol}?num_levels=3
GET /api/charting/channels/{symbol}?window=20
```

---

## Technical Indicators

### Available Indicators

#### Volatility Indicators
- **ATR (Average True Range)** - Measures market volatility
- **Bollinger Bands** - Shows overbought/oversold levels with dynamic bands

#### Trend Indicators
- **ADX (Average Directional Index)** - Measures trend strength
- **MACD** - Moving Average Convergence Divergence
- **Ichimoku Cloud** - Comprehensive trend analysis indicator
- **SMA Crossover** - 50-day and 200-day moving average crossover

#### Momentum Indicators
- **RSI (Relative Strength Index)** - Identifies overbought/oversold conditions
- **Stochastic Oscillator** - Measures momentum and reversal points

#### Volume Indicators
- **OBV (On Balance Volume)** - Shows volume-based price trends
- **VWAP (Volume Weighted Average Price)** - Fair value reference

### Usage
```
In advanced chart:
1. Click on indicator buttons (MACD, RSI, etc.)
2. Customize parameters (period, bands, etc.)
3. Multiple indicators can be overlayed
4. Click X to remove indicators
```

### API Endpoints
```
GET /api/indicators/atr/{symbol}?period=14
GET /api/indicators/adx/{symbol}?period=14
GET /api/indicators/ichimoku/{symbol}
GET /api/indicators/obv/{symbol}
GET /api/indicators/vwap/{symbol}
GET /api/indicators/macd/{symbol}?fast=12&slow=26&signal=9
GET /api/indicators/stochastic/{symbol}?period=14
GET /api/indicators/bollinger-bands/{symbol}?period=20&std_dev=2
```

---

## Stock Screener

### Features
- **Price Filters**
  - Minimum and maximum price
  - Market cap range
  - Volume requirements

- **Technical Filters**
  - RSI oversold/overbought
  - SMA crossover (bullish/bearish)
  - P/E ratio thresholds

- **Batch Processing**
  - Screen multiple stocks at once
  - Get comprehensive results with all metrics

### Usage
```
Navigate to /screener
1. Enter stock symbols (comma-separated): AAPL, MSFT, GOOGL
2. Set price range (optional)
3. Set P/E ratio max (optional)
4. Check RSI conditions (optional)
5. Select SMA crossover preference (optional)
6. Click "Run Screen"
```

### Example Criteria
```json
{
  "price_min": 50,
  "price_max": 300,
  "market_cap_min": 1000000000,
  "pe_ratio_max": 25,
  "min_volume": 1000000,
  "rsi_oversold": true,
  "sma_crossover": "bullish"
}
```

### API Endpoints
```
GET /api/screener/stock-info/{symbol}
GET /api/screener/screen?symbols=AAPL&symbols=MSFT&price_min=100&sma_crossover=bullish
GET /api/screener/rsi/{symbol}?period=14
GET /api/screener/sma-crossover/{symbol}
GET /api/screener/top-gainers?limit=10
GET /api/screener/top-losers?limit=10
GET /api/screener/most-active?limit=10
```

---

## Paper Trading

### Features
- **Virtual Trading**
  - Buy/sell stocks with simulated money
  - Default $100,000 starting capital
  - Real-time P&L calculations

- **Position Management**
  - Track open positions
  - Monitor average cost and current value
  - Unrealized P&L per position

- **Trade History**
  - Complete trade history with entry/exit prices
  - Realized P&L per trade
  - Return percentage calculations

- **Performance Metrics**
  - Total return and return %
  - Win rate calculation
  - Maximum drawdown analysis
  - Profit factor (gross profit / gross loss)

- **Position Sizing**
  - Risk-based position sizing
  - Account percentage calculator
  - 2% default risk per trade

### Usage
```
Navigate to /paper-trading
1. Enter symbol, quantity, and price
2. Click Buy or Sell button
3. Monitor portfolio value in summary cards
4. View open positions table
5. Check trade history and metrics
6. Reset account if needed
```

### API Endpoints
```
POST /api/paper-trading/buy
  {
    "symbol": "AAPL",
    "quantity": 10,
    "price": 150.50
  }

POST /api/paper-trading/sell
  {
    "symbol": "AAPL",
    "quantity": 5,
    "price": 155.00
  }

GET /api/paper-trading/portfolio-value
GET /api/paper-trading/positions
GET /api/paper-trading/trade-history
GET /api/paper-trading/performance
POST /api/paper-trading/position-sizing?account_risk_percent=2&symbol=AAPL
POST /api/paper-trading/reset?initial_cash=100000
```

---

## Backtesting Engine

### Features
- **Pre-built Strategies**
  - **RSI Strategy**: Buy when RSI < 30, Sell when RSI > 70
  - **SMA Crossover**: Buy when 50-day SMA > 200-day SMA
  - Customizable parameters

- **Performance Metrics**
  - Total trades and win rate
  - Total P&L and return %
  - Maximum drawdown analysis
  - Sharpe ratio calculation
  - Profit factor

- **Visual Results**
  - Equity curve chart
  - Portfolio value growth
  - Trade-by-trade breakdown

- **Strategy Comparison**
  - Compare RSI vs SMA strategies on same stock
  - Side-by-side performance metrics

### Usage
```
Navigate to /backtest
1. Enter stock symbol (e.g., AAPL)
2. Select strategy (RSI or SMA Crossover)
3. Set start and end dates
4. Click "Run Backtest"
5. View equity curve and metrics
6. Optionally compare with other strategy
```

### Interpretation Guide

**Win Rate**: % of profitable trades
```
High win rate (>60%) = Consistent strategy
Low win rate (<40%) = Needs refinement
```

**Profit Factor**: Gross Profit / Gross Loss
```
> 2.0 = Excellent
1.5-2.0 = Good
1.0-1.5 = Fair
< 1.0 = Losing strategy
```

**Max Drawdown**: Largest peak-to-trough decline
```
< 10% = Excellent
10-20% = Good
20-30% = Acceptable
> 30% = High risk
```

**Sharpe Ratio**: Risk-adjusted return
```
> 2.0 = Excellent
1.0-2.0 = Good
0.5-1.0 = Fair
< 0.5 = Poor
```

### API Endpoints
```
GET /api/backtest/rsi-strategy/{symbol}?start_date=2023-01-01&end_date=2024-01-01

GET /api/backtest/sma-crossover/{symbol}?start_date=2023-01-01&end_date=2024-01-01&fast_period=50&slow_period=200

GET /api/backtest/compare-strategies/{symbol}?start_date=2023-01-01&end_date=2024-01-01

POST /api/backtest/run
  {
    "symbol": "AAPL",
    "start_date": "2023-01-01",
    "end_date": "2024-01-01",
    "strategy": "rsi",
    "initial_capital": 100000
  }
```

---

## Backend Services

### Structure
```
app/
├── services/
│   ├── charting_service.py      # Chart generation
│   ├── advanced_indicators.py   # Technical indicators
│   ├── screener_service.py      # Stock screening
│   ├── paper_trading_service.py # Virtual trading
│   └── backtesting_service.py   # Strategy backtesting
├── controllers/
│   ├── charting.py              # Chart endpoints
│   ├── indicators_advanced.py   # Indicator endpoints
│   ├── screener.py              # Screener endpoints
│   ├── paper_trading.py         # Trading endpoints
│   └── backtest.py              # Backtest endpoints
```

### Integration
To use in main FastAPI app, add to `main.py`:
```python
from app.controllers import charting, indicators_advanced, screener, paper_trading, backtest

app.include_router(charting.router)
app.include_router(indicators_advanced.router)
app.include_router(screener.router)
app.include_router(paper_trading.router)
app.include_router(backtest.router)
```

---

## Frontend Pages

### New Routes
```
/charts              - Advanced charting page
/screener           - Stock screener page
/paper-trading      - Paper trading dashboard
/backtest           - Backtesting engine
```

### Navigation
All pages are accessible from the sidebar in the Layout component.

---

## Dependencies Added

### Backend (`requirements.txt`)
- **charting**: pandas, numpy
- **indicators**: scipy, statsmodels
- **screener**: yfinance data
- **backtesting**: backtesting library
- **data**: beautifulsoup4, lxml

### Frontend (`package.json`)
- **charting**: chart.js, react-chartjs-2, recharts
- **ui**: framer-motion, react-hot-toast
- **export**: html2canvas, jspdf, papaparse

---

## Quick Start

### 1. Install Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Update Main.py
Add router includes for all new controllers

### 3. Run Application
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 4. Access Features
- Dashboard: http://localhost:5173
- Charts: http://localhost:5173/charts
- Screener: http://localhost:5173/screener
- Paper Trading: http://localhost:5173/paper-trading
- Backtesting: http://localhost:5173/backtest

---

## Best Practices

### Paper Trading
- Start with small positions (1-5 shares)
- Test strategies over at least 3-6 months of data
- Track all trades and analyze patterns

### Backtesting
- Always validate with recent data
- Test during different market conditions
- Consider transaction costs in real trading
- Avoid curve-fitting (over-optimization)

### Stock Screening
- Combine multiple filters for better results
- Use in conjunction with technical analysis
- Review fundamentals before trading
- Don't rely solely on screener results

---

## Support & Troubleshooting

### Common Issues

**"Symbol not found"**
- Verify stock ticker is correct (case-insensitive)
- Check market is open during data fetch
- Try a well-known symbol (AAPL, MSFT)

**"Insufficient data"**
- Extend backtest date range
- Ensure sufficient historical data exists
- Check internet connection

**"No matches in screener"**
- Relax filter criteria
- Try different combinations
- Add additional symbols

---

## Future Enhancements

Potential features to add:
- Custom strategy builder (drag-and-drop)
- Real-time alerts (email, push notifications)
- Portfolio rebalancing suggestions
- Options analysis tools
- Multi-timeframe analysis
- Risk metrics dashboard
- Export reports (PDF, Excel)

---

## License & Credits

Built with:
- FastAPI (Python backend)
- React (JavaScript frontend)
- yfinance (Market data)
- Recharts & Chart.js (Visualizations)

