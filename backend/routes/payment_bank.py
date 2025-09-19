from fastapi import APIRouter, HTTPException, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from models.payment import Payment
from models.api_key import APIKey
from models.user import User
from uuid import uuid4
import requests, os

router = APIRouter()

SCB_CLIENT_ID = os.getenv("SCB_CLIENT_ID")
SCB_CLIENT_SECRET = os.getenv("SCB_CLIENT_SECRET")
SCB_ACCOUNT_ID = os.getenv("SCB_ACCOUNT_ID")

@router.post("/create-invoice")
def create_invoice(user_email: str, plan: str, db: Session = Depends(get_db)):
    amount = {"starter":100, "pro":300, "enterprise":1000}[plan]
    # สร้าง Invoice และ QR Code ผ่าน SCB API
    qr_response = requests.post(
        "https://api-sandbox.partners.scb/partners/v1/payment-qr",
        headers={
            "Authorization": f"Bearer {SCB_CLIENT_ID}:{SCB_CLIENT_SECRET}"
        },
        json={
            "accountId": SCB_ACCOUNT_ID,
            "amount": amount,
            "ref1": user_email
        }
    ).json()
    return {"qr_code_url": qr_response.get("qrImageURL"), "amount": amount}

@router.post("/verify-payment")
def verify_payment(user_email: str, amount: float, db: Session = Depends(get_db)):
    # ตรวจสอบ Transaction ผ่าน SCB API
    tx_response = requests.get(f"https://api-sandbox.partners.scb/partners/v1/transactions?accountId={SCB_ACCOUNT_ID}&ref1={user_email}").json()
    matched = any(tx['amount']==amount for tx in tx_response.get("transactions", []))
    if not matched:
        raise HTTPException(status_code=400, detail="Payment not found")
    
    user = db.query(User).filter(User.email==user_email).first()
    if not user:
        user = User(email=user_email, hashed_password="bank_user")
        db.add(user)
        db.commit()
        db.refresh(user)

    # สร้าง API Key อัตโนมัติ
    new_key = str(uuid4())
    api_key = APIKey(user_id=user.id, key=new_key)
    db.add(api_key)
    db.commit()

    # บันทึก Payment
    payment_record = Payment(user_id=user.id, amount=amount, currency="THB", status="success")
    db.add(payment_record)
    db.commit()

    return {"status":"success","api_key":new_key}
