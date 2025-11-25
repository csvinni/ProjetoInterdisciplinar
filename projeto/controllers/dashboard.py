from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from database import get_session
from auth.routes import get_current_user
from models import Campanha  # importe seu modelo de campanha

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # 1. Obtém o ID do Admin logado
    admin_id = user.get("id") 
    
    # 2. Filtra as campanhas pelo admin_id
    statement = select(Campanha).where(Campanha.admin_id == admin_id)
    campanhas = session.exec(statement).all()
    
    return templates.TemplateResponse(
        "card_campanha.html",
        {"request": request, "user": user, "campanhas": campanhas}
    )