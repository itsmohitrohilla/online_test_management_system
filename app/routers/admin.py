from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db

router = APIRouter()

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

security = HTTPBasic()

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == ADMIN_USERNAME and credentials.password == ADMIN_PASSWORD:
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

@router.post("/admin/create_question", response_model=schemas.QuizCreate)
def create_question(
    question: str, 
    answer: str, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    quiz = schemas.QuizCreate(admin_username=ADMIN_USERNAME, question=question, answer=answer)
    return crud.create_quiz(db, quiz=quiz)

@router.get("/admin/read_questions")
def read_questions(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    return crud.get_quiz(db, skip=skip, limit=limit)

@router.put("/admin/update_question/{quiz_id}")
def update_question(
    quiz_id: int,
    question: str,
    answer: str,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    quiz = schemas.QuizUpdate(question=question, answer=answer)
    return crud.update_quiz(db, quiz_id=quiz_id, quiz=quiz)

@router.delete("/admin/delete_question/{quiz_id}")
def delete_question(
    quiz_id: int, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    return crud.delete_quiz(db, quiz_id=quiz_id)
