from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserLogin, UserOut
from crud.user import create_user, authenticate_user, get_user_by_email
from auth.jwt import create_access_token
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from auth.deps import get_current_user
from schemas.user import UserOut


router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(400, "Email já está em uso")
    novo = create_user(db, user.nome, user.email, user.senha)
    return novo

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.senha)
    if not user:
        raise HTTPException(401, "Email ou senha incorretos")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}



@router.get("/me", response_model=UserOut)
def get_me(user = Depends(get_current_user)):
    return user