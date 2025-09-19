from fastapi import APIRouter
import stripe, os

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/create-checkout-session")
def create_checkout_session(data: dict):
    plan = data.get("plan", "starter")
    price_id = {
        "starter": "price_Starter",
        "pro": "price_Pro",
        "enterprise": "price_Enterprise"
    }.get(plan, "price_Starter")

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{'price': price_id, 'quantity': 1}],
        success_url='https://yourdomain.com/dashboard',
        cancel_url='https://yourdomain.com'
    )
    return {"checkout_url": session.url}
