from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ROTAS EXISTENTES (HOME e INDEX)
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

# ----------------------------------------------------------------------
# NOVAS ROTAS PARA LOGIN E CADASTRO
# ----------------------------------------------------------------------

@app.get("/login")
def login_page(request: Request):
    """
    Rota para a página de Login.
    URL: http://127.0.0.1:8000/login
    """
    return templates.TemplateResponse(
        "login.html",  # Rendeiza o HTML do Login
        {"request": request}
    )

@app.get("/cadastro")
def cadastro_page(request: Request):
    """
    Rota para a página de Cadastro.
    URL: http://127.0.0.1:8000/cadastro
    """
    return templates.TemplateResponse(
        "cadastro.html",  # Rendeiza o HTML do Cadastro
        {"request": request}
    )