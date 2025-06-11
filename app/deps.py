"""임시 인증용 스텁 — 실제 OAuth 구현 전까지 guest 1명을 반환"""
from .database import SessionLocal
from .models import User

def get_current_user_stub():
    db = SessionLocal()
    try:
        user = db.query(User).first()
        if not user:
            user = User(email="guest@example.com", nickname="Guest", provider="guest")
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    finally:
        db.close()
