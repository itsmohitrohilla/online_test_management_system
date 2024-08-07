from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db

router = APIRouter()

@router.post("/user/create_user", response_model=schemas.UserCreate)
def create_user(
    username: str = Query(...), 
    password: str = Query(...), 
    db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = schemas.UserCreate(username=username, password=password)
    return crud.create_user(db, user=user)

@router.get("/user/take_test")
def take_test(
    username: str = Query(...), 
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.get_quiz_only_question(db)

@router.post("/user/submit_answer")
def submit_answer(
    username: str = Query(...), 
    question_id: int = Query(...), 
    answer: str = Query(...), 
    db: Session = Depends(get_db)
):
    result = crud.submit_answer(db, username=username, question_id=question_id, answer=answer)
    if result == "Limit Over":
        raise HTTPException(status_code=400, detail="Submission limit is over")
    if not result:
        raise HTTPException(status_code=400, detail="Answer submission failed or user not found")
    return {"message": "Answer submitted successfully"}

@router.get("/user/score")
def get_score(
    username: str = Query(...), 
    db: Session = Depends(get_db)
):
    score = crud.get_user_score(db, username=username)
    if score is None:
        raise HTTPException(status_code=400, detail="User not found")
    return {"username": username, "score": score}
