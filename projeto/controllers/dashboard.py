from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import get_session
from sqlmodel import Session
# mais imports se precisar pegar dados de campanhas, etc.

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def dashboard_home(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("home.html", {"request": request})
