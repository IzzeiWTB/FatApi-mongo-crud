# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_collections, close_mongo_connection
from routers.users import router as users_router
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager para gerenciar o ciclo de vida da aplicação.
    - Na inicialização (`yield` antes): conecta ao MongoDB e cria coleções/índices.
    - No encerramento (`yield` depois): fecha a conexão com o MongoDB.
    """
    logger.info("Iniciando a aplicação...")
    await create_db_and_collections()
    yield
    logger.info("Encerrando a aplicação...")
    await close_mongo_connection()

# Cria a instância da aplicação FastAPI com o lifespan definido
app = FastAPI(
    title="API de Usuários com FastAPI e MongoDB",
    description="Uma API para realizar operações CRUD em usuários, com filtros e paginação.",
    version="1.0.0",
    lifespan=lifespan
)

# Inclui o roteador de usuários na aplicação principal
# Todas as rotas definidas em `users_router` terão o prefixo "/users"
app.include_router(users_router, prefix="/users", tags=["Users"])

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint raiz para verificar se a API está no ar.
    """
    return {"message": "Bem-vindo à API de Usuários! Acesse /docs para a documentação interativa."}

