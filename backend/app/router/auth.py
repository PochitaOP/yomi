from fastapi import APIRouter,Depends,status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2, exception_check

router = APIRouter(
        tags = ["Authentication"]
        )

@router.post("/login/", response_model=schemas.Token)
def authenticate(login: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == login.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Incorrect username or password")
    if not utils.verify(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Incorrect username or password")

    access_token = oauth2.gen_access_token(data = {"user_id" : user.id})
    return {"access_token": access_token, "token_type": "bearer"}
