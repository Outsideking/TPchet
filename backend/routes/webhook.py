from fastapi import APIRouter, Request, HTTPException, Depends
import stripe
import os
from db.database import get_db
from sqlalchemy.orm import Session
from models.payment import Payment
from models.api_key import APIKey
from models.user import User
from uuid import uuid4

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email')
        amount_total = session.get('amount_total') / 100  # USD
        system_revenue = amount_total * 0.3  # เก็บ 30%

        # หา user จาก email
        user = db.query(User).filter(User.email==customer_email).first()
        if not user:
            # สร้าง user ถ้าไม่เจอ
            user = User(email=customer_email, hashed_password="stripe_user")
            db.add(user)
            db.commit()
            db.refresh(user)

        # บันทึก payment
        payment_record = Payment(
            user_id=user.id,
            amount=system_revenue,
            currency="USD",
            status="success"
        )
        db.add(payment_record)
        db.commit()

        # สร้าง API Key
        new_key = str(uuid4())
        api_key = APIKey(user_id=user.id, key=new_key)
        db.add(api_key)
        db.commit()

        print(f"Payment success. API Key {new_key} created for {customer_email}")

    return {"status": "success"}
