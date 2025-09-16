from fastapi import FastAPI
from database import create_db_and_tables
from controllers import campanhas, doacoes  
from auth.auth import router as auth_router

app = FastAPI(title="API de Doações")

# Evento para criar o banco e as tabelas quando a aplicação iniciar
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Inclui as rotas do módulo campanhas
app.include_router(campanhas.router, prefix="/campanhas", tags=["Campanhas"])

# Inclui as rotas do módulo doacoes
app.include_router(doacoes.router, prefix="/doacoes", tags=["Doações"])

# Inclui as rotas de autenticação (cadastro e login)
app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])



# Rota raiz simples para teste
@app.get("/")
def raiz():
    return {"msg": "API de Doações está online!"}