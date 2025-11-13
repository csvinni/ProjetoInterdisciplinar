from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from typing import List
from datetime import date
from models import Doacao, Doador, Campanha
from database import get_session

router = APIRouter(prefix="/doacoes", tags=["Doações"])
templates = Jinja2Templates(directory="templates")


# 1️⃣ Formulário de cadastro
@router.get("/cadastro", response_class=HTMLResponse, name="formulario_doacao")
def formulario_doacao(request: Request, session: Session = Depends(get_session)):
    doadores = session.exec(select(Doador)).all()
    campanhas = session.exec(select(Campanha)).all()
    return templates.TemplateResponse(
        "cadastro_doacoes.html",
        {"request": request, "doadores": doadores, "campanhas": campanhas},
    )


# 2️⃣ Cadastro (POST)
@router.post("/cadastro")
def cadastrar_doacao(
    id_doador: int = Form(...),
    id_campanha: int = Form(...),
    tipo_doacao: str = Form(...),
    valor: str = Form(None),
    tipo_item: str = Form(None),
    quantidade: str = Form(None),
    data_doacao_dinheiro: str = Form(None),
    data_doacao_itens: str = Form(None),
    session: Session = Depends(get_session),
):
    # Conversões seguras
    valor = float(valor) if valor else None
    quantidade = int(quantidade) if quantidade else None

    doador_existente = session.get(Doador, id_doador)
    campanha_existente = session.get(Campanha, id_campanha)

    if not doador_existente or not campanha_existente:
        raise HTTPException(status_code=404, detail="Doador ou campanha não encontrados")

    if tipo_doacao == "dinheiro":
        data_doacao = (
            date.fromisoformat(data_doacao_dinheiro)
            if data_doacao_dinheiro
            else date.today()
        )
    else:
        data_doacao = (
            date.fromisoformat(data_doacao_itens)
            if data_doacao_itens
            else date.today()
        )

    nova_doacao = Doacao(
        id_doador=id_doador,
        id_campanha=id_campanha,
        tipo_doacao=tipo_doacao,
        valor=valor,
        tipo_item=tipo_item,
        quantidade=quantidade,
        data_doacao=data_doacao,
        status="confirmada",
    )

    session.add(nova_doacao)
    session.commit()

    return RedirectResponse(url="/dashboard", status_code=303)



# 3️⃣ Página de sucesso
@router.get("/sucesso", response_class=HTMLResponse)
def sucesso(request: Request):
    return templates.TemplateResponse("card_campanha.html", {"request": request})


# 4️⃣ Listagem
@router.get("/", response_model=List[Doacao])
def listar_doacoes(session: Session = Depends(get_session)):
    return session.exec(select(Doacao)).all()
