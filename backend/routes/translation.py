from fastapi import APIRouter, Depends
from models.api_key import APIKey
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/")
def translate(text: str, target_lang: str, db: Session = Depends(get_db), api_key: str = None):
    key = db.query(APIKey).filter(APIKey.key==api_key).first()
    if not key:
        return {"error": "Invalid API Key"}
    # ตัวอย่าง translation
    translated_text = text[::-1]  # placeholder แปลกลับข้อความ
    return {"translated": translated_text}
