from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import schemas, models, utils, oauth2, exception_check
from ..database import get_db

router = APIRouter(
        prefix = "/user",
        tags = ["Users"])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(_user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Handle error when username/email is already taken
    #user = db.query(models.User).filter(models.User.email == _user.email).first()
    #if user.username == _user.username or user.email == _user.email:
    #    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                        detail="Username/Email already taken")
    hashed_password = utils.hash(_user.password)
    _user.password = hashed_password
    user = models.User(**_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    exception_check.not_found_exception_check(user, id)

    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    exception_check.not_found_exception_check(user, id)
    exception_check.not_authorized_exception_check(user.id, user_id.id)

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
