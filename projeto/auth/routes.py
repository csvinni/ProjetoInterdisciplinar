from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from starlette.status import HTTP_302_FOUND
from models import Admin
from database import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="templates")

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
    return RedirectResponse("/dashboard", status_code=302)


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
