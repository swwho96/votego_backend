from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user_stub

router = APIRouter()

@router.post("/", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user_stub)):
    
    db_post = models.Post(title=post.title,
                          category=post.category,
                          user_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    db.add_all([models.Option(text=o.text, post_id=db_post.id)
                for o in post.options])
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/", response_model=list[schemas.PostOut])
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).options(selectinload(models.Post.options)).all()
    return posts


@router.get("/{post_id}/detail")
def post_detail(post_id: int, db: Session = Depends(get_db)):
    post = (db.query(models.Post)
              .filter(models.Post.id == post_id)
              .options(selectinload(models.Post.options)
                       .selectinload(models.Option.votes))
              .first())
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    total_votes = sum(len(opt.votes) for opt in post.options) or 1
    percentages = {opt.id: round(len(opt.votes) / total_votes * 100, 1)
                   for opt in post.options}

    return {"post": post, "percentages": percentages}



@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_stub),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(post)
    db.commit()
    return