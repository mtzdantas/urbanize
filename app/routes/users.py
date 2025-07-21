from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.login import Login
from schemas.user import UserCreate, UserResponse, UserUpdate
from utils.security import hash_password

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(Login).filter(Login.username == user.id_login.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já cadastrado")
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    
    if db.query(User).filter(User.celular == user.celular).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Celular já está em uso")
        
    new_login = Login(
        username=user.id_login.username,
        senha_hash=hash_password(user.id_login.senha)
    )

    db.add(new_login)
    db.commit()
    db.refresh(new_login)
    
    new_user = User(
        username=user.username,
        email=user.email,
        celular=user.celular,
        id_login=new_login.id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    login = db.query(Login).filter(Login.id == user.id_login).first()

    if user_data.email:
        if db.query(User).filter(User.email == user_data.email, User.id != user_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado por outro usuário")
    if user_data.celular:
        if db.query(User).filter(User.celular == user_data.celular, User.id != user_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Celular já está em uso por outro usuário")
    if user_data.id_login and user_data.id_login.username:
        if db.query(Login).filter(Login.username == user_data.id_login.username, Login.id != user.id_login).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já cadastrado por outro usuário")
        
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.celular is not None:
        user.celular = user_data.celular

    if user_data.id_login:
        if user_data.id_login.username is not None:
            login.username = user_data.id_login.username
        if user_data.id_login.senha is not None:
            login.senha_hash = hash_password(user_data.id_login.senha)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    db.delete(user)
    db.commit()
    return {"detail": "Usuário deletado com sucesso"}
