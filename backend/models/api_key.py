from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    quota = Column(Integer, default=1000)
    usage = Column(Integer, default=0)
