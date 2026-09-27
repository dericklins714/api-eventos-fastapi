from datetime import date, time
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

CATEGORIAS_VALIDAS = {
    "Palestra",
    "Workshop",
    "Minicurso",
    "Seminário",
    "Competição"
}

class EventoBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150)
    descricao: str = Field(..., min_length=1, max_length=500)
    data: date
    horario: time
    local: str = Field(..., min_length=1, max_length=150)
    capacidade: int = Field(..., gt=0)
    categoria: str = Field(..., min_length=1)

    @field_validator("titulo", "descricao", "local", "categoria")
    @classmethod
    def nao_pode_ser_vazio(cls, valor: str):
        valor = valor.strip()
        if not valor:
            raise ValueError("O campo não pode ser vazio.")
        return valor

    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls, valor: str):
        if valor not in CATEGORIAS_VALIDAS:
            raise ValueError(
                f"Categoria inválida. Use uma destas: {', '.join(sorted(CATEGORIAS_VALIDAS))}."
            )
        return valor

class EventoCreate(EventoBase):
    pass

class EventoUpdate(EventoBase):
    pass

class Evento(EventoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
