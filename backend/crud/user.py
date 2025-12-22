from sqlalchemy.orm import Session
from backend.models.user import User
from backend.auth.hash import hash_password, verify_password


def create_user(db: Session, nome: str, email: str, senha: str):
    hashed = hash_password(senha)
    user = User(nome=nome, email=email, senha=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, senha: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(senha, user.senha):
        return None
    return user
