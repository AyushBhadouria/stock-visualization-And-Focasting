# Stock Visualization & Forecasting Platform

Complete MVC-structured platform for stock analysis and forecasting.

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Architecture
- Backend: FastAPI (MVC pattern)
- Frontend: React (Component-based)
- Database: PostgreSQL + Redis
- Real-time: WebSocket