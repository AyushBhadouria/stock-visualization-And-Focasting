"""
Paper trading and portfolio simulation service
"""
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import yfinance as yf
from enum import Enum


class OrderType(str, Enum):
    BUY = "buy"
    SELL = "sell"


class Order:
    """Represents a trade order"""
    def __init__(self, order_id: str, symbol: str, order_type: OrderType, 
                 quantity: int, price: float, timestamp: datetime):
        self.order_id = order_id
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.value = quantity * price
    
    def to_dict(self) -> Dict:
        return {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "type": self.order_type.value,
            "quantity": self.quantity,
            "price": float(self.price),
            "value": float(self.value),
            "timestamp": self.timestamp.isoformat()
        }


class PaperTradingService:
    """Simulate trading without real money"""
    
    def __init__(self, initial_cash: float = 100000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Dict[str, Any]] = {}  # {symbol: {qty, avg_price, current_price}}
        self.order_history: List[Order] = []
        self.trades: List[Dict] = []  # Completed round-trip trades
    
    def buy(self, symbol: str, quantity: int, price: float, order_id: str = None) -> Optional[Order]:
        """Buy shares"""
        cost = quantity * price
        
        if cost > self.cash:
            return None
        
        self.cash -= cost
        
        if symbol not in self.positions:
            self.positions[symbol] = {
                "quantity": 0,
                "avg_price": 0,
                "entry_price": price,
                "entry_date": datetime.now()
            }
        
        pos = self.positions[symbol]
        total_qty = pos["quantity"] + quantity
        
        # Update average price
        pos["avg_price"] = ((pos["quantity"] * pos["avg_price"]) + cost) / total_qty
        pos["quantity"] = total_qty
        pos["current_price"] = price
        
        order = Order(
            order_id=order_id or f"BUY_{symbol}_{len(self.order_history)}",
            symbol=symbol,
            order_type=OrderType.BUY,
            quantity=quantity,
            price=price,
            timestamp=datetime.now()
        )
        
        self.order_history.append(order)
        return order
    
    def sell(self, symbol: str, quantity: int, price: float, order_id: str = None) -> Optional[Order]:
        """Sell shares"""
        if symbol not in self.positions or self.positions[symbol]["quantity"] < quantity:
            return None
        
        proceeds = quantity * price
        self.cash += proceeds
        
        pos = self.positions[symbol]
        
        # Calculate P&L for this trade
        cost_basis = quantity * pos["avg_price"]
        pnl = proceeds - cost_basis
        pnl_percent = (pnl / cost_basis * 100) if cost_basis > 0 else 0
        
        # Record completed trade
        self.trades.append({
            "symbol": symbol,
            "quantity": quantity,
            "buy_price": pos["avg_price"],
            "sell_price": price,
            "pnl": pnl,
            "pnl_percent": pnl_percent,
            "exit_date": datetime.now()
        })
        
        # Update position
        pos["quantity"] -= quantity
        pos["current_price"] = price
        
        if pos["quantity"] == 0:
            del self.positions[symbol]
        
        order = Order(
            order_id=order_id or f"SELL_{symbol}_{len(self.order_history)}",
            symbol=symbol,
            order_type=OrderType.SELL,
            quantity=quantity,
            price=price,
            timestamp=datetime.now()
        )
        
        self.order_history.append(order)
        return order
    
    def get_portfolio_value(self) -> Dict[str, float]:
        """Calculate current portfolio value"""
        stocks_value = sum(
            pos["quantity"] * pos["current_price"]
            for pos in self.positions.values()
        )
        
        total_value = self.cash + stocks_value
        
        return {
            "cash": float(self.cash),
            "stocks_value": float(stocks_value),
            "total_value": float(total_value),
            "return": float(total_value - self.initial_cash),
            "return_percent": float((total_value - self.initial_cash) / self.initial_cash * 100)
        }
    
    def get_positions(self) -> List[Dict]:
        """Get current positions"""
        positions = []
        for symbol, pos in self.positions.items():
            positions.append({
                "symbol": symbol,
                "quantity": pos["quantity"],
                "avg_price": float(pos["avg_price"]),
                "current_price": float(pos.get("current_price", 0)),
                "value": float(pos["quantity"] * pos.get("current_price", 0)),
                "unrealized_pnl": float(pos["quantity"] * (pos.get("current_price", 0) - pos["avg_price"]))
            })
        return positions
    
    def get_trade_history(self) -> List[Dict]:
        """Get completed trades"""
        return self.trades
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Calculate performance metrics"""
        if not self.trades:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "total_pnl": 0,
                "avg_win": 0,
                "avg_loss": 0,
                "profit_factor": 0
            }
        
        trades_df = pd.DataFrame(self.trades)
        
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df["pnl"] > 0])
        losing_trades = len(trades_df[trades_df["pnl"] < 0])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = trades_df["pnl"].sum()
        avg_win = trades_df[trades_df["pnl"] > 0]["pnl"].mean() if winning_trades > 0 else 0
        avg_loss = abs(trades_df[trades_df["pnl"] < 0]["pnl"].mean()) if losing_trades > 0 else 0
        
        profit_factor = avg_win / avg_loss if avg_loss != 0 else 0
        
        # Calculate max drawdown
        portfolio_values = [self.initial_cash]
        for trade in self.trades:
            portfolio_values.append(portfolio_values[-1] + trade["pnl"])
        
        peak = max(portfolio_values)
        drawdown = min((peak - val) / peak * 100 if peak > 0 else 0 for val in portfolio_values)
        
        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": float(win_rate),
            "total_pnl": float(total_pnl),
            "avg_win": float(avg_win),
            "avg_loss": float(avg_loss),
            "profit_factor": float(profit_factor),
            "max_drawdown": float(drawdown)
        }
    
    def position_sizing(self, account_risk_percent: float = 2.0, symbol: str = None) -> Dict[str, float]:
        """
        Calculate position sizes based on risk management
        
        account_risk_percent: % of account to risk per trade (default 2%)
        """
        portfolio_value = self.get_portfolio_value()["total_value"]
        risk_amount = portfolio_value * (account_risk_percent / 100)
        
        if symbol:
            try:
                ticker = yf.Ticker(symbol)
                current_price = ticker.info.get("currentPrice", 0)
                
                if current_price > 0:
                    position_size = int(risk_amount / current_price)
                    return {
                        "symbol": symbol,
                        "position_size": position_size,
                        "risk_amount": float(risk_amount),
                        "account_percent": float((position_size * current_price) / portfolio_value * 100)
                    }
            except:
                pass
        
        return {
            "risk_amount": float(risk_amount),
            "account_percent": float(account_risk_percent)
        }
