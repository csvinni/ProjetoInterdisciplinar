from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from typing import List
from datetime import date
from models import Doacao, Doador
from database import get_session

router = APIRouter(prefix="/doacoes", tags=["Doações"])
templates = Jinja2Templates(directory="templates")


# 🧠 1. Exibir o formulário de cadastro
@router.get("/cadastro", response_class=HTMLResponse,  name="formulario_doacao")
def formulario_doacao(request: Request, session: Session = Depends(get_session)):
    doadores = session.exec(select(Doador)).all()  # pega os doadores cadastrados
    return templates.TemplateResponse(
        "cadastro_doacoes.html", {"request": request, "doadores": doadores}
    )


# 💾 2. Cadastrar doação (POST)
@router.post("/cadastro")
def cadastrar_doacao(
    doador: int = Form(...),
    tipo_doacao: str = Form(...),
    quantidade_dinheiro: str = Form(None),
    descricao_itens: str = Form(None),
    data_doacao_dinheiro: str = Form(None),
    data_doacao_itens: str = Form(None),
    session: Session = Depends(get_session),
):
    # Verifica se o doador existe
    doador_existente = session.get(Doador, doador)
    if not doador_existente:
        raise HTTPException(status_code=404, detail="Doador não encontrado")

    # Define a data
    if tipo_doacao == "dinheiro":
        data_doacao = (
            date.fromisoformat(data_doacao_dinheiro)
            if data_doacao_dinheiro
            else date.today()
        )
        descricao = f"Doação em dinheiro: {quantidade_dinheiro}"
    else:
        data_doacao = (
            date.fromisoformat(data_doacao_itens)
            if data_doacao_itens
            else date.today()
        )
        descricao = f"Doação em itens: {descricao_itens}"

    nova_doacao = Doacao(
        doador_id=doador_existente.id,
        tipo=tipo_doacao,
        descricao=descricao,
        data_doacao=data_doacao,
    )

    session.add(nova_doacao)
    session.commit()
    session.refresh(nova_doacao)

    return RedirectResponse(url="/doacoes/sucesso", status_code=303)


# 🎉 3. Página de sucesso
@router.get("/sucesso", response_class=HTMLResponse)
def sucesso(request: Request):
    return templates.TemplateResponse("cadastro_sucesso.html", {"request": request})


# 🧾 4. (mantém suas rotas API)
@router.get("/", response_model=List[Doacao])
def listar_doacoes(session: Session = Depends(get_session)):
    return session.exec(select(Doacao)).all()
