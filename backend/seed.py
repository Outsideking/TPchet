from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.user import User
from models.api_key import APIKey
from models.translation import Translation
from models.payment import Payment
from passlib.hash import bcrypt
from datetime import datetime, timedelta

db: Session = SessionLocal()

# Users
user1 = User(email="user1@example.com", hashed_password=bcrypt.hash("password1"))
user2 = User(email="user2@example.com", hashed_password=bcrypt.hash("password2"))
admin = User(email="admin@example.com", hashed_password=bcrypt.hash("adminpass"), role="admin")
db.add_all([user1, user2, admin])
db.commit()

# API Keys
key1 = APIKey(user_id=user1.id, key="user1-key-123")
key2 = APIKey(user_id=user2.id, key="user2-key-456")
db.add_all([key1, key2])
db.commit()

# Translations
for i in range(5):
    t = Translation(user_id=user1.id, source_text=f"ข้อความ {i}", translated_text=f"Sample {i}", source_lang="th", target_lang="en", timestamp=datetime.now() - timedelta(days=i))
    db.add(t)
db.commit()

# Payments
for i in range(5):
    p = Payment(user_id=user1.id, amount=10+i, currency="USD", status="success", timestamp=datetime.now() - timedelta(days=i))
    db.add(p)
db.commit()

db.close()
