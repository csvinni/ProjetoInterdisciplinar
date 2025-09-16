# models.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel


# -----------------------------
# Admin
# -----------------------------
class Admin(SQLModel, table=True):
    __tablename__ = 'admin'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True)
    senha: str
    ong: str
    data_criacao: date = Field(default_factory=date.today)

    def set_password(self, password: str):
        self.senha = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.senha, password)


# -----------------------------
# Doador
# -----------------------------
class Doador(SQLModel, table=True):
    __tablename__ = 'doadores'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True)
    telefone: str
    senha: str
    data_criacao: date = Field(default_factory=date.today)

    doacoes: List["Doacao"] = Relationship(back_populates="doador")

    def set_password(self, password: str):
        self.senha = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.senha, password)


# -----------------------------
# Categoria
# -----------------------------
class Categoria(SQLModel, table=True):
    __tablename__ = 'categorias'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str


# -----------------------------
# Campanha
# -----------------------------
class Campanha(SQLModel, table=True):
    __tablename__ = "campanhas"

    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    meta_financeira: str
    meta_itens: str
    data_inicio: Optional[date]
    data_fim: Optional[date]
    status: str
    data_criacao: date = Field(default_factory=date.today)
    categoria_id: Optional[int] = Field(default=None, foreign_key="categorias.id")

    doacoes: List["Doacao"] = Relationship(back_populates="campanha")
    relatorios: List["Relatorio"] = Relationship(back_populates="campanha")


# -----------------------------
# Doacao
# -----------------------------
class Doacao(SQLModel, table=True):
    __tablename__ = "doacoes"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_doador: int = Field(foreign_key="doadores.id")
    id_campanha: int = Field(foreign_key="campanhas.id")
    tipo_doacao: str
    tipo_item: Optional[str]
    quantidade: Optional[int]
    valor: Optional[float]
    data_doacao: date
    status: str = "confirmada"

    doador: Optional[Doador] = Relationship(back_populates="doacoes")
    campanha: Optional[Campanha] = Relationship(back_populates="doacoes")


# -----------------------------
# Relatorio
# -----------------------------
class Relatorio(SQLModel, table=True):
    __tablename__ = "relatorios"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_campanha: int = Field(foreign_key="campanhas.id")
    data_referencia: Optional[date]
    total: Optional[float]
    total_itens_doados: int
    meta_comparativo: str

    campanha: Optional[Campanha] = Relationship(back_populates="relatorios")


# -----------------------------
# Schemas Pydantic para criação/atualização
# -----------------------------
class CampanhaCreate(BaseModel):
    titulo: str
    descricao: str
    meta_financeira: str
    meta_itens: str
    data_inicio: Optional[date]
    data_fim: Optional[date]
    status: str
    categoria_id: Optional[int]


class DoacaoCreate(BaseModel):
    id_doador: int
    id_campanha: int
    tipo_doacao: str
    tipo_item: Optional[str]
    quantidade: Optional[int]
    valor: Optional[float]
    data_doacao: date
    status: Optional[str] = "confirmada"
