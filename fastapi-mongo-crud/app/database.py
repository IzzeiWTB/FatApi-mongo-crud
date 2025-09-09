# app/database.py
import motor.motor_asyncio
from pymongo.errors import CollectionInvalid
import logging

# String de conexão com o MongoDB que será executado no contêiner do Docker
# O nome do host "mongo" é o nome do serviço definido no docker-compose.yml
MONGO_DETAILS = "mongodb://mongo:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Acessa o banco de dados chamado "userdb"
database = client.userdb

# Acessa a coleção chamada "users_collection"
users_collection = database.get_collection("users")

logger = logging.getLogger(__name__)

async def create_db_and_collections():
    """
    Função para ser chamada na inicialização da aplicação.
    Cria o banco de dados e a coleção se não existirem,
    e garante que o índice único para o campo 'email' seja criado.
    """
    try:
        # Tenta criar a coleção. Se já existir, a CollectionInvalid é levantada.
        await database.create_collection("users")
        logger.info("Coleção 'users' criada.")
    except CollectionInvalid:
        logger.info("Coleção 'users' já existe.")
        pass
    
    # Garante que o índice único em 'email' exista para evitar duplicatas.
    # `background=True` permite que o índice seja criado sem bloquear outras operações.
    await users_collection.create_index("email", unique=True, background=True)
    logger.info("Índice único para 'email' garantido.")

async def close_mongo_connection():
    """Fecha a conexão do cliente MongoDB."""
    client.close()
    logger.info("Conexão com o MongoDB fechada.")

def get_db_collection():
    """
    Função de dependência para obter a coleção do banco de dados nos endpoints.
    Embora simples, o uso de uma função de dependência facilita a testabilidade
    e a manutenção no futuro.
    """
    return users_collection
