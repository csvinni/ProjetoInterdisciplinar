from sqlmodel import SQLModel, create_engine, Session

# Substitua pelo caminho do seu banco, ex: SQLite local ou PostgreSQL
DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session