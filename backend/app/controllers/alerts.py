from fastapi import APIRouter, Depends, HTTPException
from app.controllers.auth import get_current_user
from app.config.mongodb import alerts_collection
from pydantic import BaseModel

router = APIRouter()

class AlertCreate(BaseModel):
    symbol: str
    condition: str  # "above" or "below"
    target_price: float

@router.get("/")
async def get_alerts(current_user: dict = Depends(get_current_user)):
    """Get user's alerts"""
    user_id = str(current_user["_id"])
    alerts = alerts_collection.find({"user_id": user_id})
    
    return {
        "alerts": [
            {
                "id": str(alert["_id"]),
                "symbol": alert["symbol"],
                "condition": alert["condition"],
                "target_price": alert["target_price"],
                "is_active": alert.get("is_active", True),
                "created_at": alert.get("created_at", "2024-01-01")
            }
            for alert in alerts
        ]
    }

@router.post("/")
async def create_alert(alert: AlertCreate, current_user: dict = Depends(get_current_user)):
    """Create a new price alert"""
    if alert.condition not in ["above", "below"]:
        raise HTTPException(status_code=400, detail="Condition must be 'above' or 'below'")
    
    user_id = str(current_user["_id"])
    
    db_alert = {
        "user_id": user_id,
        "symbol": alert.symbol.upper(),
        "condition": alert.condition,
        "target_price": alert.target_price,
        "is_active": True,
        "created_at": "2024-01-01"
    }
    
    result = alerts_collection.insert_one(db_alert)
    
    return {
        "message": f"Alert created for {alert.symbol.upper()}",
        "alert_id": str(result.inserted_id)
    }

@router.delete("/{alert_id}")
async def delete_alert(alert_id: str, current_user: dict = Depends(get_current_user)):
    """Delete an alert"""
    user_id = str(current_user["_id"])
    
    result = alerts_collection.delete_one({
        "_id": alert_id,
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {"message": "Alert deleted"}