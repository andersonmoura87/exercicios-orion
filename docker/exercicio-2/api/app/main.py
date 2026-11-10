from contextlib import asynccontextmanager
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from .database import connect, initialize


@asynccontextmanager
async def lifespan(app):
    initialize()
    yield


app = FastAPI(lifespan=lifespan)


class TarefaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")
    titulo: str = Field(min_length=1, max_length=200)

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("O título não pode ficar vazio")
        return value


class Tarefa(BaseModel):
    id: int
    titulo: str


@app.post("/tarefas", response_model=Tarefa, status_code=201)
def criar_tarefa(tarefa: TarefaEntrada):
    try:
        with connect() as conn:
            return conn.execute(
                "INSERT INTO tarefas (titulo) VALUES (%s) RETURNING id, titulo",
                (tarefa.titulo,),
            ).fetchone()
    except psycopg.Error:
        raise HTTPException(503, "Banco indisponível") from None


@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas():
    try:
        with connect() as conn:
            return conn.execute("SELECT id, titulo FROM tarefas ORDER BY id").fetchall()
    except psycopg.Error:
        raise HTTPException(503, "Banco indisponível") from None
