# app/models.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    """
    Classe personalizada para lidar com a conversão de `ObjectId` do MongoDB.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, *args, **kwargs):
        field_schema.update(type="string")


class UserBase(BaseModel):
    """Modelo base com os campos comuns do usuário."""
    name: str = Field(..., min_length=2, max_length=80, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="E-mail único do usuário")
    age: int = Field(..., ge=0, description="Idade do usuário, deve ser maior ou igual a zero")
    is_active: bool = Field(default=True, description="Status do usuário (ativo ou inativo)")


class UserCreate(UserBase):
    """Modelo para criação de um novo usuário."""
    pass


class UserUpdate(BaseModel):
    """

    Modelo para atualização de um usuário.
    Todos os campos são opcionais para permitir atualizações parciais (PATCH-like).
    """
    name: Optional[str] = Field(None, min_length=2, max_length=80)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """
    Modelo para a resposta da API. Inclui o 'id' do banco de dados.
    O alias `_id` é usado para mapear o campo do MongoDB para o campo `id` do modelo.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        # Permite que o Pydantic funcione com modelos de ORM/ODM (como os do Motor)
        from_attributes = True
        # Permite o uso de alias no mapeamento de campos
        populate_by_name = True
        # Permite a serialização de tipos como ObjectId para JSON
        json_encoders = {ObjectId: str}
