from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from starlette.status import HTTP_302_FOUND
from models import Admin
from database import get_session
from fastapi import HTTPException, status

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="templates")

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=status.HTTP_302_FOUND, headers={"Location": "/auth/login"})
    return user


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(Admin).where(Admin.email == email)).first()
    if not user or not user.check_password(senha):
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Credenciais inválidas"})
    # ✅ Guarda o usuário logado na sessão
    request.session["user"] = {"id": user.id, "email": user.email, "nome": user.nome}
    return RedirectResponse(url="/dashboard", status_code=HTTP_302_FOUND)


@router.get("/cadastro", response_class=HTMLResponse)
def cadastro_page(request: Request):
    return templates.TemplateResponse("auth/cadastro.html", {"request": request})

@router.post("/cadastro")
def cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    ong: str = Form(...),
    session: Session = Depends(get_session)
):
    # Verifica se já existe o email
    if session.exec(select(Admin).where(Admin.email == email)).first():
        return templates.TemplateResponse("auth/cadastro.html", {"request": request, "error": "Email já cadastrado."})

    novo_admin = Admin(nome=nome, email=email, ong=ong)
    novo_admin.set_password(senha)

    session.add(novo_admin)
    session.commit()
    session.refresh(novo_admin)

    return RedirectResponse("/auth/login", status_code=HTTP_302_FOUND)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()  # 🧹 Limpa os dados da sessão
    return RedirectResponse(url="/auth/login", status_code=HTTP_302_FOUND)

@router.get("/perfil", response_class=HTMLResponse)
def perfil_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("auth/perfil.html", {"request": request, "user": user})


@router.post("/perfil")
def atualizar_perfil(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(None),
    session: Session = Depends(get_session)
):
    user_data = request.session.get("user")
    user = session.get(Admin, user_data["id"])

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.nome = nome
    user.email = email

    if senha and senha.strip():
        user.set_password(senha)

    session.add(user)
    session.commit()
    session.refresh(user)

    # Atualiza sessão
    request.session["user"] = {"id": user.id, "email": user.email, "nome": user.nome}

    return RedirectResponse("/dashboard", status_code=302)


