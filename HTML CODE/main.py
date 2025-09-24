from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):
    nome = "Visitante"
    
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "usuario_nome": nome}
    )

@app.get("/index")
def index(request: Request):
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )