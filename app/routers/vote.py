from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user_stub

router = APIRouter()

@router.post("/", status_code=201)
def cast_vote(vote: schemas.VoteCreate,
              db: Session = Depends(get_db),
              current_user: models.User = Depends(get_current_user_stub)):
    
    # option 존재 여부 확인
    option = db.query(models.Option).filter(models.Option.id == vote.option_id).first()
    if option is None:
        raise HTTPException(status_code=404, detail="Option not found")

    # 같은 post에 이미 투표했는지 확인
    already = (
        db.query(models.Vote)
        .join(models.Option)
        .filter(models.Option.post_id == option.post_id,
                models.Vote.user_id == current_user.id)
        .first()
    )
    if already:
        # raise HTTPException(status_code=400, detail="이미 투표했습니다.")
        db.delete(already)

    db_vote = models.Vote(user_id=current_user.id, option_id=option.id)
    db.add(db_vote)
    db.commit()
    return {"ok": True}
