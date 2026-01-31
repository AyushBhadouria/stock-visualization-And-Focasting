import asyncio
import json
import websockets
from typing import Set, Dict
from app.services.data_service import DataService

class WebSocketService:
    def __init__(self):
        self.connections: Set[websockets.WebSocketServerProtocol] = set()
        self.subscriptions: Dict[str, Set[websockets.WebSocketServerProtocol]] = {}
        self.data_service = DataService()
        
    async def register(self, websocket: websockets.WebSocketServerProtocol):
        """Register a new WebSocket connection"""
        self.connections.add(websocket)
        print(f"Client connected. Total connections: {len(self.connections)}")
        
    async def unregister(self, websocket: websockets.WebSocketServerProtocol):
        """Unregister a WebSocket connection"""
        self.connections.discard(websocket)
        # Remove from all subscriptions
        for symbol in list(self.subscriptions.keys()):
            self.subscriptions[symbol].discard(websocket)
            if not self.subscriptions[symbol]:
                del self.subscriptions[symbol]
        print(f"Client disconnected. Total connections: {len(self.connections)}")
        
    async def subscribe(self, websocket: websockets.WebSocketServerProtocol, symbol: str):
        """Subscribe to real-time updates for a symbol"""
        if symbol not in self.subscriptions:
            self.subscriptions[symbol] = set()
        self.subscriptions[symbol].add(websocket)
        
        # Send initial quote
        quote = self.data_service.get_real_time_quote(symbol)
        if "error" not in quote:
            await websocket.send(json.dumps({
                'type': 'quote',
                'symbol': symbol,
                'data': quote
            }))
            
    async def unsubscribe(self, websocket: websockets.WebSocketServerProtocol, symbol: str):
        """Unsubscribe from updates for a symbol"""
        if symbol in self.subscriptions:
            self.subscriptions[symbol].discard(websocket)
            if not self.subscriptions[symbol]:
                del self.subscriptions[symbol]
                
    async def broadcast_quote(self, symbol: str, quote_data: dict):
        """Broadcast quote update to all subscribers"""
        if symbol in self.subscriptions:
            message = json.dumps({
                'type': 'quote',
                'symbol': symbol,
                'data': quote_data
            })
            
            # Send to all subscribers
            disconnected = set()
            for websocket in self.subscriptions[symbol]:
                try:
                    await websocket.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(websocket)
                    
            # Clean up disconnected clients
            for websocket in disconnected:
                await self.unregister(websocket)
                
    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, message: str):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            action = data.get('action')
            symbol = data.get('symbol', '').upper()
            
            if action == 'subscribe' and symbol:
                await self.subscribe(websocket, symbol)
                await websocket.send(json.dumps({
                    'type': 'status',
                    'message': f'Subscribed to {symbol}'
                }))
                
            elif action == 'unsubscribe' and symbol:
                await self.unsubscribe(websocket, symbol)
                await websocket.send(json.dumps({
                    'type': 'status',
                    'message': f'Unsubscribed from {symbol}'
                }))
                
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': 'Invalid JSON message'
            }))
            
    async def start_price_updates(self):
        """Start periodic price updates for subscribed symbols"""
        while True:
            for symbol in list(self.subscriptions.keys()):
                quote = self.data_service.get_real_time_quote(symbol)
                if "error" not in quote:
                    await self.broadcast_quote(symbol, quote)
            
            await asyncio.sleep(30)  # Update every 30 seconds

# Global WebSocket service instance
websocket_service = WebSocketService()