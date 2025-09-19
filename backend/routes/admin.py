from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.api_key import APIKey
from models.translation import Translation
from models.payment import Payment
from sqlalchemy import func
import uuid

router = APIRouter()

# Generate API Key
@router.post("/generate-key/{user_id}")
def generate_key(user_id: int, db: Session = Depends(get_db)):
    new_key = str(uuid.uuid4())
    api_key = APIKey(user_id=user_id, key=new_key)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return {"api_key": api_key.key, "quota": api_key.quota}

# List all keys
@router.get("/keys")
def list_keys(db: Session = Depends(get_db)):
    return db.query(APIKey).all()

# Translation report
@router.get("/translations")
def translations_report(db: Session = Depends(get_db)):
    result = db.query(
        func.date(Translation.timestamp).label("date"),
        func.count(Translation.id).label("count")
    ).group_by(func.date(Translation.timestamp)).all()
    return [{"date": str(r.date), "count": r.count} for r in result]

# Payment report
@router.get("/payments")
def payments_report(db: Session = Depends(get_db)):
    result = db.query(
        func.date(Payment.timestamp).label("date"),
        func.sum(Payment.amount).label("amount")
    ).group_by(func.date(Payment.timestamp)).all()
    return [{"date": str(r.date), "amount": float(r.amount)} for r in result]
