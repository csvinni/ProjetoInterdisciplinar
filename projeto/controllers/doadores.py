from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from models import Doador
from database import get_session

router = APIRouter(prefix="/doadores", tags=["Doadores"])
templates = Jinja2Templates(directory="templates")


# Página HTML do cadastro de doador
@router.get("/cadastro", response_class=HTMLResponse)
def exibir_formulario(request: Request):
    return templates.TemplateResponse("cadastro_doador.html", {"request": request})


# Rota POST para receber o cadastro do formulário
@router.post("/cadastro")
def cadastrar_doador(
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    session: Session = Depends(get_session),
):
    # Verificar se já existe doador com o mesmo e-mail
    doador_existente = session.exec(select(Doador).where(Doador.email == email)).first()
    if doador_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_doador = Doador(nome=nome, email=email, telefone=telefone)
    session.add(novo_doador)
    session.commit()
    session.refresh(novo_doador)

    # Redireciona para uma página de sucesso ou lista de doadores
    return RedirectResponse(url="/dashboard", status_code=303)

