from fastapi import FastAPI
from routes import auth, admin, payment, translation

app = FastAPI(title="TPchet API")

app.include_router(auth.router, prefix="/auth")
app.include_router(admin.router, prefix="/admin")
app.include_router(payment.router, prefix="/payment")
app.include_router(translation.router, prefix="/translate")
