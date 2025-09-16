from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models import Admin, Doador
from database import get_session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
from datetime import datetime, timedelta
from typing import Union

SECRET_KEY = "chave_supersecreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/auth", tags=["Autenticação"])

def criar_token(dado: dict, tempo_exp: Union[int, None] = None):
    to_encode = dado.copy()
    exp = datetime.utcnow() + timedelta(minutes=tempo_exp or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------------------------
# Cadastro de Administrador
# ---------------------------
@router.post("/admin/cadastro")
def cadastrar_admin(admin: Admin, session: Session = Depends(get_session)):
    existente = session.exec(select(Admin).where(Admin.email == admin.email)).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    admin.set_password(admin.senha)
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return {"msg": "Administrador cadastrado com sucesso!"}


# ---------------------------
# Cadastro de Doador
# ---------------------------
@router.post("/doador/cadastro")
def cadastrar_doador(doador: Doador, session: Session = Depends(get_session)):
    existente = session.exec(select(Doador).where(Doador.email == doador.email)).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    doador.set_password(doador.senha)
    session.add(doador)
    session.commit()
    session.refresh(doador)
    return {"msg": "Doador cadastrado com sucesso!"}


# ---------------------------
# Login (Admin ou Doador)
# ---------------------------
@router.post("/login")
def login(email: str, senha: str, session: Session = Depends(get_session)):
    # Tenta encontrar o usuário como admin
    usuario = session.exec(select(Admin).where(Admin.email == email)).first()
    tipo_usuario = "admin"

    if not usuario:
        usuario = session.exec(select(Doador).where(Doador.email == email)).first()
        tipo_usuario = "doador"

    if not usuario or not usuario.check_password(senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({"sub": str(usuario.id), "tipo": tipo_usuario})
    return {"access_token": token, "token_type": "bearer"}
