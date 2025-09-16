from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Doacao
from database import get_session
from typing import List

router = APIRouter(prefix="/doacoes", tags=["Doações"])


@router.post("/", response_model=Doacao)
def criar_doacao(doacao: Doacao, session: Session = Depends(get_session)):
    session.add(doacao)
    session.commit()
    session.refresh(doacao)
    return doacao


@router.get("/", response_model=List[Doacao])
def listar_doacoes(session: Session = Depends(get_session)):
    return session.exec(select(Doacao)).all()


@router.get("/{doacao_id}", response_model=Doacao)
def obter_doacao(doacao_id: int, session: Session = Depends(get_session)):
    doacao = session.get(Doacao, doacao_id)
    if not doacao:
        raise HTTPException(status_code=404, detail="Doação não encontrada")
    return doacao


@router.put("/{doacao_id}", response_model=Doacao)
def atualizar_doacao(doacao_id: int, dados: Doacao, session: Session = Depends(get_session)):
    doacao = session.get(Doacao, doacao_id)
    if not doacao:
        raise HTTPException(status_code=404, detail="Doação não encontrada")
    for key, value in dados.dict(exclude_unset=True).items():
        setattr(doacao, key, value)
    session.add(doacao)
    session.commit()
    session.refresh(doacao)
    return doacao


@router.delete("/{doacao_id}")
def deletar_doacao(doacao_id: int, session: Session = Depends(get_session)):
    doacao = session.get(Doacao, doacao_id)
    if not doacao:
        raise HTTPException(status_code=404, detail="Doação não encontrada")
    session.delete(doacao)
    session.commit()
    return {"ok": True, "msg": "Doação deletada"}