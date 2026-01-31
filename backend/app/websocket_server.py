import asyncio
import websockets
from app.services.websocket_service import websocket_service

async def websocket_handler(websocket, path):
    """Handle WebSocket connections"""
    await websocket_service.register(websocket)
    try:
        async for message in websocket:
            await websocket_service.handle_message(websocket, message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await websocket_service.unregister(websocket)

async def start_websocket_server():
    """Start WebSocket server"""
    # Start price update task
    asyncio.create_task(websocket_service.start_price_updates())
    
    # Start WebSocket server
    server = await websockets.serve(websocket_handler, "localhost", 8001)
    print("WebSocket server started on ws://localhost:8001")
    return server

if __name__ == "__main__":
    asyncio.run(start_websocket_server())