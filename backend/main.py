from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import auth, stocks, indicators, forecasts, watchlist, alerts, currency
import uvicorn

# Try importing new controllers with error handling
try:
    from app.controllers import charting
    HAS_CHARTING = True
except Exception as e:
    print(f"Warning: Could not import charting controller: {e}")
    HAS_CHARTING = False

try:
    from app.controllers import indicators_advanced
    HAS_IND_ADV = True
except Exception as e:
    print(f"Warning: Could not import indicators_advanced controller: {e}")
    HAS_IND_ADV = False

try:
    from app.controllers import screener
    HAS_SCREENER = True
except Exception as e:
    print(f"Warning: Could not import screener controller: {e}")
    HAS_SCREENER = False

try:
    from app.controllers import paper_trading
    HAS_PT = True
except Exception as e:
    print(f"Warning: Could not import paper_trading controller: {e}")
    HAS_PT = False

try:
    from app.controllers import backtest
    HAS_BT = True
except Exception as e:
    print(f"Warning: Could not import backtest controller: {e}")
    HAS_BT = False

app = FastAPI(title="Stock Platform API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with trailing slashes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(indicators.router, prefix="/api/indicators", tags=["indicators"])
app.include_router(forecasts.router, prefix="/api/forecasts", tags=["forecasts"])
app.include_router(watchlist.router, prefix="/api/watchlist", tags=["watchlist"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(currency.router, prefix="/api/currency", tags=["currency"])

# Include new routers if available
if HAS_CHARTING:
    app.include_router(charting.router)
if HAS_IND_ADV:
    app.include_router(indicators_advanced.router)
if HAS_SCREENER:
    app.include_router(screener.router)
if HAS_PT:
    app.include_router(paper_trading.router)
if HAS_BT:
    app.include_router(backtest.router)

@app.get("/")
async def root():
    return {"message": "Stock Platform API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)