from sqlalchemy.orm import Session
from . import models, schemas

def create_quiz(db: Session, quiz: schemas.QuizCreate):
    db_quiz = models.Quiz(admin_username=quiz.admin_username, question=quiz.question, answer=quiz.answer)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def get_quiz(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Quiz).offset(skip).limit(limit).all()

def get_quiz_only_question(db: Session):
    quizzes = db.query(models.Quiz.id, models.Quiz.question).all()
    return [{"id": quiz.id, "question": quiz.question} for quiz in quizzes]

def update_quiz(db: Session, quiz_id: int, quiz: schemas.QuizUpdate):
    db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if db_quiz:
        db_quiz.question = quiz.question
        db_quiz.answer = quiz.answer
        db.commit()
        db.refresh(db_quiz)
    return db_quiz

def delete_quiz(db: Session, quiz_id: int):
    db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if db_quiz:
        db.delete(db_quiz)
        db.commit()
    return db_quiz

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def submit_answer(db: Session, username: str, question_id: int, answer: str):
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if user.submit_count >= 10:
        return "Limit Over"

    quiz = db.query(models.Quiz).filter(models.Quiz.id == question_id).first()
    if not quiz or quiz.answer != answer:
        return None

    user.submit_count += 1
    user.score += quiz.marks
    db.commit()
    db.refresh(user)
    return user

def get_user_score(db: Session, username: str):
    user = get_user_by_username(db, username=username)
    return user.score if user else None
