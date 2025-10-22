from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import get_session
from sqlmodel import Session
from auth.routes import get_current_user  # importa a função

# mais imports se precisar pegar dados de campanhas, etc.

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
def dashboard(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("historico.html", {"request": request, "user": user})

