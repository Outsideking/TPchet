from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import get_db
from models.translation import Translation

router = APIRouter()

class TranslateRequest(BaseModel):
    user_id: int
    text: str
    source_lang: str
    target_lang: str

@router.post("/")
def translate(req: TranslateRequest, db: Session = Depends(get_db)):
    # ตัวอย่างแปลง่าย ๆ (mock)
    result = f"{req.text} translated to {req.target_lang}"
    translation_record = Translation(
        user_id=req.user_id,
        source_text=req.text,
        translated_text=result,
        source_lang=req.source_lang,
        target_lang=req.target_lang
    )
    db.add(translation_record)
    db.commit()
    db.refresh(translation_record)
    return {"translated_text": result}
