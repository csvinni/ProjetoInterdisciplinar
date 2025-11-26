from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlmodel import Session, select
from models import Campanha
from database import get_session
from datetime import date
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from auth.routes import get_current_user

router = APIRouter(prefix="/campanhas", tags=["Campanhas"])
templates = Jinja2Templates(directory="templates")


# -------------------------------------------------------------------
# 🔹 CADASTRAR CAMPANHA
# -------------------------------------------------------------------
@router.post("/cadastro_campanha")
def cadastro_campanha(
    titulo: str = Form(...),
    descricao: str = Form(...),
    meta_financeira: float = Form(...),
    meta_itens: int = Form(...),
    data_inicio: date = Form(...),
    data_fim: date = Form(...),
    status: str = Form(...),
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    nova_campanha = Campanha(
        titulo=titulo,
        descricao=descricao,
        meta_financeira=meta_financeira,
        meta_itens=meta_itens,
        data_inicio=data_inicio,
        data_fim=data_fim,
        status=status,
        admin_id=user["id"]
    )

    session.add(nova_campanha)
    session.commit()
    session.refresh(nova_campanha)

    return {"message": "Campanha criada com sucesso!", "campanha": nova_campanha}


# -------------------------------------------------------------------
# 🔹 EDITAR CAMPANHA (POST)
# -------------------------------------------------------------------
@router.post("/editar/{campanha_id}")
def editar_campanha_via_post(
    campanha_id: int,
    titulo: str = Form(...),
    descricao: str = Form(...),
    meta_financeira: float = Form(...),
    meta_itens: int = Form(...),
    data_inicio: date = Form(...),
    data_fim: date = Form(...),
    status: str = Form(...),
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    campanha = session.get(Campanha, campanha_id)

    if not campanha or campanha.admin_id != user["id"]:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    campanha.titulo = titulo
    campanha.descricao = descricao
    campanha.meta_financeira = meta_financeira
    campanha.meta_itens = meta_itens
    campanha.data_inicio = data_inicio
    campanha.data_fim = data_fim
    campanha.status = status

    session.add(campanha)
    session.commit()
    session.refresh(campanha)

    return {"message": "Campanha atualizada com sucesso!", "campanha": campanha}


# -------------------------------------------------------------------
# 🔹 DELETAR CAMPANHA (POST)
# -------------------------------------------------------------------
@router.post("/deletar/{campanha_id}")
def deletar_campanha_via_post(
    campanha_id: int,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    campanha = session.get(Campanha, campanha_id)

    if not campanha or campanha.admin_id != user["id"]:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    session.delete(campanha)
    session.commit()

    return RedirectResponse(url="/campanhas/", status_code=303)


# -------------------------------------------------------------------
# 🔹 LISTAGEM PRINCIPAL (SOMENTE DO USUÁRIO)
# -------------------------------------------------------------------
@router.get("/", response_class=HTMLResponse)
def listar_campanhas(
    request: Request,
    search: str | None = None,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    query = select(Campanha).where(Campanha.admin_id == user["id"])

    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Campanha.titulo.ilike(search_term)) |
            (Campanha.descricao.ilike(search_term))
        )

    campanhas = session.exec(query).all()

    return templates.TemplateResponse(
        "card_campanha.html",
        {"request": request, "campanhas": campanhas, "search": search}
    )


# -------------------------------------------------------------------
# 🔹 LISTAR CAMPANHAS ATIVAS
# -------------------------------------------------------------------
@router.get("/ativas", response_class=HTMLResponse)
def listar_campanhas_ativas(
    request: Request,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    campanhas = session.exec(
        select(Campanha).where(
            Campanha.status.ilike("ativa"),
            Campanha.admin_id == user["id"]
        )
    ).all()

    return templates.TemplateResponse("card_campanha.html", {"request": request, "campanhas": campanhas})


# -------------------------------------------------------------------
# 🔹 LISTAR CAMPANHAS CONCLUÍDAS
# -------------------------------------------------------------------
@router.get("/concluidas", response_class=HTMLResponse)
def listar_campanhas_concluidas(
    request: Request,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    campanhas = session.exec(
        select(Campanha).where(
            Campanha.status.ilike("concluida"),
            Campanha.admin_id == user["id"]
        )
    ).all()

    return templates.TemplateResponse("card_campanha.html", {"request": request, "campanhas": campanhas})


# -------------------------------------------------------------------
# 🔹 OBTER CAMPANHA POR ID
# -------------------------------------------------------------------
@router.get("/{campanha_id}", response_model=Campanha)
def obter_campanha(
    campanha_id: int,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    campanha = session.get(Campanha, campanha_id)

    if not campanha or campanha.admin_id != user["id"]:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    return campanha
