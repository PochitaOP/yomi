from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import schemas, models, oauth2, exception_check
from ..database import get_db

router = APIRouter(
        prefix = "/messages",
        tags = ["Message"]
        )

#get all chatroom
#create room
#delete room
#find room by id

# get all messages
@router.get("/")
async def get_messages(db: Session = Depends(get_db), user_id : int =  Depends(oauth2.get_current_user)):
    messages = db.query(models.Message).all()
    return messages

# add new message from user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MessageOut) 
async def post_message(post : schemas.MessageIn, db: Session = Depends(get_db), user_id : int =  Depends(oauth2.get_current_user)):
    if user_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User does not exist")

    new_message = models.Message(user_id=user_id.id, **post.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

# get message by its id
@router.get("/{id}")
async def search_message_by_id(id : int, db: Session = Depends(get_db), user_id : int =  Depends(oauth2.get_current_user)):
    message = db.query(models.Message).filter(models.Message.id == id).first()

    exception_check.not_found_exception_check(message, id)
    return message

# search messages that contains substring
@router.get("/search/{message}")
async def search_message(message: str, db: Session = Depends(get_db), user_id : int =  Depends(oauth2.get_current_user)):
    messages = db.query(models.Message).filter(models.Message.message.contains(message)).all()

    exception_check.not_found_exception_check(messages, message)
    return messages

# search all user messages
@router.get("/search/{id}/")
async def search_user_messages(id: int, db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    message = db.query(models.Message).filter(models.Message.user_id == id).all()

    exception_check.not_found_exception_check(message, id)
    return message

# search all user messages that contain substring
@router.get("/search/{id}/{message}")
async def search_user_specific_message(id: int, message: str, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    messages = db.query(models.Message).filter(models.Message.user_id == id).filter(models.Message.message.contains(message)).all()

    exception_check.not_found_exception_check(messages, id)
    return messages

# delete message
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id : int, db: Session = Depends(get_db), user_id : int =  Depends(oauth2.get_current_user)):
    message_query = db.query(models.Message).filter(models.Message.id == id)
    message = message_query.first()

    exception_check.not_found_exception_check(message, id)
    exception_check.not_authorized_exception_check(message.user_id, user_id.id)

    message_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update message
@router.put("/{id}", response_model=schemas.MessageOut)
async def update_post(id: int, post: schemas.MessageIn, db: Session = Depends(get_db), user_id : int =  Depends(oauth2.get_current_user)):
    message_query = db.query(models.Message).filter(models.Message.id == id)
    message = message_query.first()

    exception_check.not_found_exception_check(message, id)
    exception_check.not_authorized_exception_check(message.user_id, user_id.id)

    message_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return message
