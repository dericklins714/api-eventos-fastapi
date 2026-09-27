from fastapi import APIRouter, status
from model.participante import (
    Participante,
    ParticipanteCreate,
    ParticipanteUpdate
)
from service import participante_service

router = APIRouter(prefix="/participantes", tags=["Participantes"])

@router.post(
    "",
    response_model=Participante,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_participante(dados: ParticipanteCreate):
    return participante_service.cadastrar_participante(dados)

@router.get("", response_model=list[Participante])
def listar_participantes():
    return participante_service.listar_participantes()

@router.get("/{participante_id}", response_model=Participante)
def consultar_participante(participante_id: int):
    return participante_service.buscar_participante_ou_erro(participante_id)

@router.put("/{participante_id}", response_model=Participante)
def atualizar_participante(
    participante_id: int,
    dados: ParticipanteUpdate
):
    return participante_service.atualizar_participante(
        participante_id,
        dados
    )

@router.delete(
    "/{participante_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_participante(participante_id: int):
    participante_service.excluir_participante(participante_id)
