from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Campanha, CampanhaCreate
from database import get_session
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Form
from datetime import date
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse


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
    session: Session = Depends(get_session)
):
    nova_campanha = Campanha(
        titulo=titulo,
        descricao=descricao,
        meta_financeira=meta_financeira,
        meta_itens=meta_itens,
        data_inicio=data_inicio,
        data_fim=data_fim,
        status=status
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