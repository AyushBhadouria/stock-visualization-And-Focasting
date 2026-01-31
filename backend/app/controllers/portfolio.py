from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.config.database import get_db
from app.controllers.auth import get_current_user
from app.models.user import User
from app.models.portfolio import Portfolio, Transaction
from app.services.data_service import DataService
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter()
data_service = DataService()

class TransactionCreate(BaseModel):
    symbol: str
    transaction_type: str  # "buy" or "sell"
    quantity: float
    price: float
    transaction_date: datetime

@router.get("/")
async def get_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's portfolio summary"""
    # Get or create portfolio
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    if not portfolio:
        portfolio = Portfolio(user_id=current_user.id)
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
    
    # Get all transactions
    transactions = db.query(Transaction).filter(Transaction.portfolio_id == portfolio.id).all()
    
    # Calculate holdings
    holdings = {}
    for transaction in transactions:
        symbol = transaction.symbol
        if symbol not in holdings:
            holdings[symbol] = {'quantity': 0, 'total_cost': 0}
        
        if transaction.transaction_type == 'buy':
            holdings[symbol]['quantity'] += transaction.quantity
            holdings[symbol]['total_cost'] += transaction.total_amount
        else:  # sell
            holdings[symbol]['quantity'] -= transaction.quantity
            holdings[symbol]['total_cost'] -= transaction.total_amount
    
    # Remove zero holdings
    holdings = {k: v for k, v in holdings.items() if v['quantity'] > 0}
    
    # Get current prices and calculate portfolio value
    portfolio_value = 0
    portfolio_cost = 0
    holdings_with_prices = []
    
    for symbol, holding in holdings.items():
        quote = data_service.get_real_time_quote(symbol)
        current_price = quote.get('price', 0)
        
        current_value = holding['quantity'] * current_price
        avg_cost = holding['total_cost'] / holding['quantity'] if holding['quantity'] > 0 else 0
        gain_loss = current_value - holding['total_cost']
        gain_loss_percent = (gain_loss / holding['total_cost'] * 100) if holding['total_cost'] > 0 else 0
        
        holdings_with_prices.append({
            'symbol': symbol,
            'quantity': holding['quantity'],
            'avg_cost': avg_cost,
            'current_price': current_price,
            'current_value': current_value,
            'total_cost': holding['total_cost'],
            'gain_loss': gain_loss,
            'gain_loss_percent': gain_loss_percent
        })
        
        portfolio_value += current_value
        portfolio_cost += holding['total_cost']
    
    total_gain_loss = portfolio_value - portfolio_cost
    total_gain_loss_percent = (total_gain_loss / portfolio_cost * 100) if portfolio_cost > 0 else 0
    
    return {
        'portfolio_id': portfolio.id,
        'total_value': portfolio_value,
        'total_cost': portfolio_cost,
        'total_gain_loss': total_gain_loss,
        'total_gain_loss_percent': total_gain_loss_percent,
        'holdings': holdings_with_prices
    }

@router.post("/transaction")
async def add_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new transaction"""
    # Get or create portfolio
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    if not portfolio:
        portfolio = Portfolio(user_id=current_user.id)
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
    
    # Validate transaction
    if transaction.transaction_type not in ['buy', 'sell']:
        raise HTTPException(status_code=400, detail="Transaction type must be 'buy' or 'sell'")
    
    if transaction.quantity <= 0 or transaction.price <= 0:
        raise HTTPException(status_code=400, detail="Quantity and price must be positive")
    
    # Create transaction
    total_amount = transaction.quantity * transaction.price
    db_transaction = Transaction(
        portfolio_id=portfolio.id,
        symbol=transaction.symbol.upper(),
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity,
        price=transaction.price,
        total_amount=total_amount,
        transaction_date=transaction.transaction_date
    )
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return {
        'message': f'Transaction added: {transaction.transaction_type} {transaction.quantity} shares of {transaction.symbol.upper()}',
        'transaction_id': db_transaction.id
    }

@router.get("/transactions")
async def get_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get transaction history"""
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    if not portfolio:
        return {'transactions': []}
    
    transactions = db.query(Transaction).filter(
        Transaction.portfolio_id == portfolio.id
    ).order_by(Transaction.transaction_date.desc()).all()
    
    return {
        'transactions': [
            {
                'id': t.id,
                'symbol': t.symbol,
                'type': t.transaction_type,
                'quantity': t.quantity,
                'price': t.price,
                'total_amount': t.total_amount,
                'date': t.transaction_date
            }
            for t in transactions
        ]
    }