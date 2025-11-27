from fastapi import APIRouter, Depends, HTTPException, Request, Form, Query
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

# 5️⃣ Página de histórico (HTML)
@router.get("/historico", response_class=HTMLResponse)
def historico_doacoes(
    request: Request,
    campanha_id: str | None = Query(None),
    doador_id: str | None = Query(None),
    tipo: str | None = Query(None),
    data: str | None = Query(None),
    session: Session = Depends(get_session),
):
    # converter ids para int com segurança
    campanha_id_int: int | None = None
    doador_id_int: int | None = None

    try:
        if campanha_id not in (None, ""):
            campanha_id_int = int(campanha_id)
    except ValueError:
        campanha_id_int = None

    try:
        if doador_id not in (None, ""):
            doador_id_int = int(doador_id)
    except ValueError:
        doador_id_int = None

    # Base da query
    query = (
        select(Doacao, Doador, Campanha)
        .join(Doador, Doacao.id_doador == Doador.id)
        .join(Campanha, Doacao.id_campanha == Campanha.id)
    )

    # Filtros opcionais (usando as versões int convertidas)
    if campanha_id_int:
        query = query.where(Doacao.id_campanha == campanha_id_int)

    if doador_id_int:
        query = query.where(Doacao.id_doador == doador_id_int)

    if tipo:
        query = query.where(Doacao.tipo_doacao == tipo)

    if data:
        from datetime import date
        try:
            data_formatada = date.fromisoformat(data)
            query = query.where(Doacao.data_doacao == data_formatada)
        except ValueError:
            # data inválida -> ignora o filtro
            pass

    resultados = session.exec(query).all()

    lista_doacoes = []
    for doacao, doador, campanha in resultados:
        lista_doacoes.append({
            "nome_doador": doador.nome,
            "campanha": campanha.titulo,
            "data": doacao.data_doacao.strftime("%d/%m/%Y"),
            "tipo": doacao.tipo_doacao,
            "valor": doacao.valor,
            "quantidade": doacao.quantidade,
            "descricao": doacao.tipo_item,
        })

    # Para preencher os selects
    campanhas = session.exec(select(Campanha)).all()
    doadores = session.exec(select(Doador)).all()

    return templates.TemplateResponse(
        "historico.html",
        {
            "request": request,
            "doacoes": lista_doacoes,
            "campanhas": campanhas,
            "doadores": doadores,
        },
    )

@router.get("/campanha/{campanha_id}/modal", response_class=HTMLResponse)
def historico_campanha_modal(
    campanha_id: int,
    request: Request,
    session: Session = Depends(get_session),
    
):

    campanha = session.get(Campanha, campanha_id)

    if not campanha or campanha.admin_id != user["id"]:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    doacoes = session.exec(
        select(Doacao).where(Doacao.campanha_id == campanha_id)
    ).all()

    return templates.TemplateResponse(
        "partials/historico_modal.html",
        {
            "request": request,
            "doacoes": doacoes,
            "nome_campanha": campanha.nome
        }
    )

