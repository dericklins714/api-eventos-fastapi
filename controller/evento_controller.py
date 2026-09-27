from fastapi import APIRouter, status
from model.evento import Evento, EventoCreate, EventoUpdate
from service import evento_service
from service import participante_service

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post(
    "",
    response_model=Evento,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_evento(dados: EventoCreate):
    return evento_service.cadastrar_evento(dados)

@router.get("", response_model=list[Evento])
def listar_eventos():
    return evento_service.listar_eventos()

@router.get("/{evento_id}", response_model=Evento)
def consultar_evento(evento_id: int):
    return evento_service.buscar_evento(evento_id)

@router.put("/{evento_id}", response_model=Evento)
def atualizar_evento(evento_id: int, dados: EventoUpdate):
    return evento_service.atualizar_evento(evento_id, dados)

@router.delete(
    "/{evento_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_evento(evento_id: int):
    evento_service.excluir_evento(evento_id)

@router.post(
    "/{evento_id}/inscricoes/{participante_id}",
    status_code=status.HTTP_201_CREATED
)
def inscrever_participante(evento_id: int, participante_id: int):
    participante = participante_service.buscar_participante(participante_id)

    return evento_service.inscrever_participante(
        evento_id,
        participante_id,
        participante
    )

@router.get("/{evento_id}/inscricoes", response_model=list)
def listar_inscritos(evento_id: int):
    return evento_service.listar_inscritos(
        evento_id,
        participante_service.buscar_participante
    )
