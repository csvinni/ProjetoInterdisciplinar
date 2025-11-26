from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Campanha, CampanhaCreate
from database import get_session
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Form
from datetime import date
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from auth.routes import get_current_user


router = APIRouter(prefix="/campanhas", tags=["Campanhas"])
templates = Jinja2Templates(directory="templates")


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
    admin_id = user.get("id")
    nova_campanha = Campanha(
        titulo=titulo,
        descricao=descricao,
        meta_financeira=meta_financeira,
        meta_itens=meta_itens,
        data_inicio=data_inicio,
        data_fim=data_fim,
        status=status,
        admin_id=admin_id
    )
    session.add(nova_campanha)
    session.commit()
    session.refresh(nova_campanha)
    # Garante que o objeto retornado seja um dicionário/JSON (o JavaScript espera isso)
    return {"message": "Campanha criada com sucesso!", "campanha": nova_campanha}

# @router.get("/cadastro_campanha", response_class=HTMLResponse)
# def mostrar_formulario(request: Request):
#     return templates.TemplateResponse("cadastro_campanha.html", {"request": request})


@router.get("/{campanha_id}", response_model=Campanha)
def obter_campanha(campanha_id: int, session: Session = Depends(get_session)):
    campanha = session.get(Campanha, campanha_id)
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    return campanha


@router.put("/{campanha_id}", response_model=Campanha)
def atualizar_campanha(campanha_id: int, dados: Campanha, session: Session = Depends(get_session)):
    campanha = session.get(Campanha, campanha_id)
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    for key, value in dados.dict(exclude_unset=True).items():
        setattr(campanha, key, value)
    session.add(campanha)
    session.commit()
    session.refresh(campanha)
    return campanha


@router.delete("/{campanha_id}")
def deletar_campanha(campanha_id: int, session: Session = Depends(get_session)):
    campanha = session.get(Campanha, campanha_id)
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    session.delete(campanha)
    session.commit()
    return {"ok": True, "msg": "Campanha deletada"}

@router.post("/deletar/{campanha_id}")
def deletar_campanha_via_post(campanha_id: int, session: Session = Depends(get_session)):
    campanha = session.get(Campanha, campanha_id)
    
    if not campanha:
        # Se não encontrar, lança exceção (ou pode ser um RedirectResponse com mensagem de erro)
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    
    # Lógica de exclusão
    session.delete(campanha)
    session.commit()
    
    # Redireciona o usuário de volta para a página de listagem de campanhas
    # Altere o "/campanhas/" se o caminho da sua listagem for outro (ex: "/")
    return RedirectResponse(url="/campanhas/", status_code=303)

@router.get("/", response_class=HTMLResponse)
def listar_campanhas(
    request: Request, 
    search: str | None = None,
    session: Session = Depends(get_session)
):
    query = select(Campanha)

    # Se houver termo de busca, filtra
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Campanha.titulo.ilike(search_term)) |
            (Campanha.descricao.ilike(search_term))
        )

    campanhas = session.exec(query).all()

    return templates.TemplateResponse(
        "card_campanha.html",
        {
            "request": request,
            "campanhas": campanhas,
            "search": search  # opcional para mostrar no template
        }
    )


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
    session: Session = Depends(get_session)
):
    campanha = session.get(Campanha, campanha_id)
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    
    # Atualiza os campos da campanha com os dados do formulário
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
    
    # Retorna JSON para ser processado pelo JavaScript
    return {"message": "Campanha atualizada com sucesso!", "campanha": campanha}


router = APIRouter(prefix="/campanhas", tags=["Campanhas"])
templates = Jinja2Templates(directory="templates")


# 🔹 1 — Listar campanhas ativas
@router.get("/ativas", response_class=HTMLResponse, name="listar_campanhas_ativas")
def listar_campanhas_ativas(request: Request, session: Session = Depends(get_session)):
    campanhas = session.exec(
        select(Campanha).where(Campanha.status.ilike("ativa"))
    ).all()

    return templates.TemplateResponse(
        "card_campanha.html",
        {"request": request, "campanhas": campanhas}
    )


# 🔹 2 — Listar campanhas concluídas
@router.get("/concluidas", response_class=HTMLResponse, name="listar_campanhas_concluidas")
def listar_campanhas_concluidas(request: Request, session: Session = Depends(get_session)):
    campanhas = session.exec(
        select(Campanha).where(Campanha.status.ilike("concluida"))
    ).all()

    return templates.TemplateResponse(
        "card_campanha.html",
        {"request": request, "campanhas": campanhas}
    )


# 🔹 3 — Listar todas (página principal)
@router.get("/", response_class=HTMLResponse)
def listar_campanhas(
    request: Request, 
    search: str | None = None,
    session: Session = Depends(get_session)
):
    query = select(Campanha)

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


# ❗️ AGORA SIM — rota dinâmica por último
@router.get("/{campanha_id}", response_model=Campanha)
def obter_campanha(campanha_id: int, session: Session = Depends(get_session)):
    campanha = session.get(Campanha, campanha_id)
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    return campanha