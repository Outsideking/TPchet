from fastapi import APIRouter
import stripe
import os

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/create-checkout-session")
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': 1000,
                'product_data': {'name': 'TPchet Pro Plan'}
            },
            'quantity': 1
        }],
        mode='payment',
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel",
    )
    return {"checkout_url": session.url}
