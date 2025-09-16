from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Campanha, CampanhaCreate
from database import get_session
from typing import List

router = APIRouter(prefix="/campanhas", tags=["Campanhas"])


@router.post("/", response_model=Campanha)
def criar_campanha(campanha: CampanhaCreate, session: Session = Depends(get_session)):
    nova_campanha = Campanha(**campanha.dict())
    session.add(nova_campanha)
    session.commit()
    session.refresh(nova_campanha)
    return nova_campanha


@router.get("/", response_model=List[Campanha])
def listar_campanhas(session: Session = Depends(get_session)):
    campanhas = session.exec(select(Campanha)).all()
    return campanhas


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