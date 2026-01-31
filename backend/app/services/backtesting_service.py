"""
Backtesting engine for strategy testing
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Callable
import yfinance as yf
from datetime import datetime


class BacktestResult:
    """Holds backtesting results"""
    def __init__(self):
        self.trades = []
        self.equity_curve = []
        self.portfolio_values = []
        self.dates = []
    
    def to_dict(self) -> Dict:
        return {
            "trades": self.trades,
            "equity_curve": self.equity_curve,
            "portfolio_values": self.portfolio_values,
            "dates": [d.isoformat() if isinstance(d, datetime) else str(d) for d in self.dates],
            "metrics": self.calculate_metrics()
        }
    
    def calculate_metrics(self) -> Dict[str, float]:
        """Calculate performance metrics"""
        if not self.trades or not self.portfolio_values:
            return {}
        
        trades_df = pd.DataFrame(self.trades)
        
        # Basic metrics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df["pnl"] > 0])
        losing_trades = len(trades_df[trades_df["pnl"] < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # P&L metrics
        total_pnl = trades_df["pnl"].sum()
        gross_profit = trades_df[trades_df["pnl"] > 0]["pnl"].sum()
        gross_loss = abs(trades_df[trades_df["pnl"] < 0]["pnl"].sum())
        
        profit_factor = gross_profit / gross_loss if gross_loss != 0 else 0
        
        # Drawdown
        cumulative = np.cumsum(self.equity_curve)
        if len(cumulative) > 0:
            running_max = np.maximum.accumulate(cumulative)
            drawdown = (running_max - cumulative) / running_max
            max_drawdown = np.max(drawdown) * 100 if len(drawdown) > 0 else 0
        else:
            max_drawdown = 0
        
        # Return metrics
        initial_capital = 100000
        final_value = self.portfolio_values[-1] if self.portfolio_values else initial_capital
        total_return = (final_value - initial_capital) / initial_capital * 100
        
        # Sharpe Ratio (simplified - using daily returns)
        if len(self.equity_curve) > 1:
            daily_returns = np.diff(self.equity_curve) / self.equity_curve[:-1]
            if np.std(daily_returns) > 0:
                sharpe_ratio = (np.mean(daily_returns) / np.std(daily_returns)) * np.sqrt(252)
            else:
                sharpe_ratio = 0
        else:
            sharpe_ratio = 0
        
        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": float(win_rate),
            "total_pnl": float(total_pnl),
            "gross_profit": float(gross_profit),
            "gross_loss": float(gross_loss),
            "profit_factor": float(profit_factor),
            "max_drawdown": float(max_drawdown),
            "total_return_percent": float(total_return),
            "sharpe_ratio": float(sharpe_ratio),
            "final_portfolio_value": float(final_value)
        }


class BacktestingEngine:
    """Simple backtesting engine for strategies"""
    
    @staticmethod
    def backtest_rsi_strategy(symbol: str, start_date: str, end_date: str,
                             rsi_oversold: int = 30, rsi_overbought: int = 70,
                             initial_capital: float = 100000) -> BacktestResult:
        """
        Backtest a simple RSI strategy:
        - Buy when RSI < oversold (default 30)
        - Sell when RSI > overbought (default 70)
        """
        result = BacktestResult()
        
        # Fetch data
        try:
            data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        except:
            return result
        
        if data.empty:
            return result
        
        # Calculate RSI
        closes = data["Close"]
        delta = closes.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Simulation
        position = 0
        entry_price = 0
        portfolio_value = initial_capital
        cash = initial_capital
        
        for i in range(1, len(data)):
            date = data.index[i]
            price = closes.iloc[i]
            rsi_value = rsi.iloc[i]
            
            # Buy signal
            if position == 0 and rsi_value < rsi_oversold:
                position = int(cash / price)
                entry_price = price
                cash -= position * price
            
            # Sell signal
            elif position > 0 and rsi_value > rsi_overbought:
                pnl = position * (price - entry_price)
                cash += position * price
                
                result.trades.append({
                    "entry_price": float(entry_price),
                    "exit_price": float(price),
                    "quantity": position,
                    "pnl": float(pnl),
                    "pnl_percent": float(pnl / (position * entry_price) * 100) if position * entry_price > 0 else 0
                })
                
                position = 0
            
            # Calculate equity
            if position > 0:
                stock_value = position * price
                portfolio_value = cash + stock_value
            else:
                portfolio_value = cash
            
            result.portfolio_values.append(portfolio_value)
            result.equity_curve.append(portfolio_value - initial_capital)
            result.dates.append(date)
        
        return result
    
    @staticmethod
    def backtest_sma_crossover(symbol: str, start_date: str, end_date: str,
                              fast_period: int = 50, slow_period: int = 200,
                              initial_capital: float = 100000) -> BacktestResult:
        """
        Backtest SMA crossover strategy:
        - Buy when SMA(fast) > SMA(slow)
        - Sell when SMA(fast) < SMA(slow)
        """
        result = BacktestResult()
        
        try:
            data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        except:
            return result
        
        if data.empty:
            return result
        
        closes = data["Close"]
        sma_fast = closes.rolling(window=fast_period).mean()
        sma_slow = closes.rolling(window=slow_period).mean()
        
        position = 0
        entry_price = 0
        portfolio_value = initial_capital
        cash = initial_capital
        
        for i in range(max(fast_period, slow_period), len(data)):
            date = data.index[i]
            price = closes.iloc[i]
            
            fast = sma_fast.iloc[i]
            slow = sma_slow.iloc[i]
            
            # Buy signal
            if position == 0 and fast > slow:
                position = int(cash / price)
                entry_price = price
                cash -= position * price
            
            # Sell signal
            elif position > 0 and fast < slow:
                pnl = position * (price - entry_price)
                cash += position * price
                
                result.trades.append({
                    "entry_price": float(entry_price),
                    "exit_price": float(price),
                    "quantity": position,
                    "pnl": float(pnl),
                    "pnl_percent": float(pnl / (position * entry_price) * 100) if position * entry_price > 0 else 0
                })
                
                position = 0
            
            if position > 0:
                stock_value = position * price
                portfolio_value = cash + stock_value
            else:
                portfolio_value = cash
            
            result.portfolio_values.append(portfolio_value)
            result.equity_curve.append(portfolio_value - initial_capital)
            result.dates.append(date)
        
        return result
    
    @staticmethod
    def backtest_custom(symbol: str, start_date: str, end_date: str,
                       signal_func: Callable[[pd.DataFrame, int], bool],
                       initial_capital: float = 100000) -> BacktestResult:
        """
        Backtest with custom signal function
        
        signal_func should return True for buy, False for sell/hold
        """
        result = BacktestResult()
        
        try:
            data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        except:
            return result
        
        if data.empty:
            return result
        
        position = 0
        entry_price = 0
        portfolio_value = initial_capital
        cash = initial_capital
        
        for i in range(1, len(data)):
            try:
                signal = signal_func(data, i)
                price = data["Close"].iloc[i]
                date = data.index[i]
                
                if signal and position == 0:
                    position = int(cash / price)
                    entry_price = price
                    cash -= position * price
                
                elif not signal and position > 0:
                    pnl = position * (price - entry_price)
                    cash += position * price
                    
                    result.trades.append({
                        "entry_price": float(entry_price),
                        "exit_price": float(price),
                        "quantity": position,
                        "pnl": float(pnl)
                    })
                    
                    position = 0
                
                if position > 0:
                    stock_value = position * price
                    portfolio_value = cash + stock_value
                else:
                    portfolio_value = cash
                
                result.portfolio_values.append(portfolio_value)
                result.equity_curve.append(portfolio_value - initial_capital)
                result.dates.append(date)
            
            except Exception as e:
                continue
        
        return result
