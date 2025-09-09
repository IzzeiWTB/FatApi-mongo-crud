from fastapi import APIRouter, HTTPException, Depends, status, Response, Query
from typing import List
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from models import UserCreate, UserUpdate, UserResponse
from database import get_db_collection
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter()

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário",
    description="Cria um novo usuário no banco de dados. O e-mail deve ser único."
)
async def create_user(
    user: UserCreate, 
    db: AsyncIOMotorCollection = Depends(get_db_collection)
):
    """
    Cria um novo usuário.
    - **user**: Dados do usuário a ser criado.
    - **Retorna**: O usuário criado com seu ID.
    - **Levanta exceção 409** se o e-mail já existir.
    """
    user_dict = user.model_dump()
    try:
        result = await db.insert_one(user_dict)
        # Busca o documento recém-criado para retornar ao cliente
        created_user = await db.find_one({"_id": result.inserted_id})
        return created_user
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"O e-mail '{user.email}' já está em uso."
        )

@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Lista todos os usuários",
    description="Retorna uma lista de usuários com suporte a filtros e paginação."
)
async def get_users(
    q: str = Query(None, description="Busca textual pelo nome do usuário (case-insensitive)"),
    min_age: int = Query(None, ge=0, description="Filtro para idade mínima"),
    max_age: int = Query(None, ge=0, description="Filtro para idade máxima"),
    is_active: bool = Query(None, description="Filtro por status de usuário ativo"),
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Número de itens por página"),
    db: AsyncIOMotorCollection = Depends(get_db_collection)
):
    """
    Lista usuários com filtros e paginação.
    """
    filters = {}
    if q:
        filters["name"] = {"$regex": q, "$options": "i"}
    if min_age is not None and max_age is not None:
        filters["age"] = {"$gte": min_age, "$lte": max_age}
    elif min_age is not None:
        filters["age"] = {"$gte": min_age}
    elif max_age is not None:
        filters["age"] = {"$lte": max_age}
    if is_active is not None:
        filters["is_active"] = is_active
    
    skip = (page - 1) * limit
    cursor = db.find(filters).sort("name", 1).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    return users

@router.get(
    "/{id}",
    response_model=UserResponse,
    summary="Busca um usuário pelo ID",
    description="Retorna os dados de um usuário específico."
)
async def get_user_by_id(
    id: str, 
    db: AsyncIOMotorCollection = Depends(get_db_collection)
):
    """
    Obtém um único usuário pelo seu ID.
    - **id**: ID do usuário (deve ser um ObjectId válido).
    - **Retorna**: O usuário encontrado.
    - **Levanta exceção 400** se o ID for inválido.
    - **Levanta exceção 404** se o usuário não for encontrado.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    user = await db.find_one({"_id": ObjectId(id)})
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com ID '{id}' não encontrado")

@router.put(
    "/{id}",
    response_model=UserResponse,
    summary="Atualiza um usuário",
    description="Atualiza os dados de um usuário existente."
)
async def update_user(
    id: str,
    user_update: UserUpdate,
    db: AsyncIOMotorCollection = Depends(get_db_collection)
):
    """
    Atualiza um usuário.
    - **id**: ID do usuário a ser atualizado.
    - **user_update**: Dados a serem atualizados (campos opcionais).
    - **Retorna**: O usuário com os dados atualizados.
    - **Levanta exceção 404** se o usuário não for encontrado.
    - **Levanta exceção 409** se o novo e-mail já pertencer a outro usuário.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")

    # `model_dump(exclude_unset=True)` cria um dict apenas com os campos que foram enviados
    update_data = user_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado para atualizar foi fornecido.")

    # Verifica se o e-mail está sendo alterado para um que já existe
    if "email" in update_data:
        if await db.find_one({"email": update_data["email"], "_id": {"$ne": ObjectId(id)}}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"O e-mail '{update_data['email']}' já está em uso.")

    result = await db.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com ID '{id}' não encontrado")
    
    updated_user = await db.find_one({"_id": ObjectId(id)})
    return updated_user

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um usuário",
    description="Remove um usuário do banco de dados."
)
async def delete_user(
    id: str, 
    db: AsyncIOMotorCollection = Depends(get_db_collection)
):
    """
    Deleta um usuário.
    - **id**: ID do usuário a ser deletado.
    - **Retorna**: Status 204 se a deleção for bem-sucedida.
    - **Levanta exceção 404** se o usuário não for encontrado.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")

    result = await db.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com ID '{id}' não encontrado")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

