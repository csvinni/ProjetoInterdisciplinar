from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables
from controllers.dashboard import router as dashboard_router
from auth.routes import router as auth_router
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI(title="API de Doações - MVC")
app.add_middleware(SessionMiddleware, secret_key="chave_super_secreta")


# Inicializa o banco
create_db_and_tables()

# Configura templates e arquivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota principal
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Inclui as rotas da pasta auth
app.include_router(auth_router)
app.include_router(dashboard_router)
