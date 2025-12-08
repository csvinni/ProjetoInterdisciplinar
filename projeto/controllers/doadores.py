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

@router.post("/cadastro")
def cadastrar_doador(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    session: Session = Depends(get_session),
):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Admin não autenticado")

    admin_id = user["id"]

    # Verificar se já existe doador com o mesmo e-mail PARA ESTE ADMIN
    doador_existente = session.exec(
        select(Doador)
        .where(Doador.email == email)
        .where(Doador.admin_id == admin_id)
    ).first()

    if doador_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado para esta ONG")

    novo_doador = Doador(
        nome=nome,
        email=email,
        telefone=telefone,
        admin_id=admin_id
    )

    session.add(novo_doador)
    session.commit()
    session.refresh(novo_doador)

    return RedirectResponse(url="/dashboard", status_code=303)
