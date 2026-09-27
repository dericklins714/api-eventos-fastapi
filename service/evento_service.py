from fastapi import HTTPException, status
from model.evento import Evento, EventoCreate, EventoUpdate

eventos: list[Evento] = []
inscricoes: list[dict] = []
proximo_id = 1

def cadastrar_evento(dados: EventoCreate) -> Evento:
    global proximo_id
    evento = Evento(id=proximo_id, **dados.model_dump())
    eventos.append(evento)
    proximo_id += 1
    return evento

def listar_eventos() -> list[Evento]:
    return eventos

def buscar_evento(evento_id: int) -> Evento:
    for evento in eventos:
        if evento.id == evento_id:
            return evento
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Evento não encontrado."
    )

def atualizar_evento(evento_id: int, dados: EventoUpdate) -> Evento:
    evento = buscar_evento(evento_id)
    dados_atualizados = dados.model_dump()

    for campo, valor in dados_atualizados.items():
        setattr(evento, campo, valor)

    return evento

def excluir_evento(evento_id: int):
    evento = buscar_evento(evento_id)
    eventos.remove(evento)

    global inscricoes
    inscricoes = [
        inscricao for inscricao in inscricoes
        if inscricao["evento_id"] != evento_id
    ]

def inscrever_participante(evento_id: int, participante_id: int, participante):
    evento = buscar_evento(evento_id)

    if participante is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante não encontrado."
        )

    for inscricao in inscricoes:
        if (
            inscricao["evento_id"] == evento_id
            and inscricao["participante_id"] == participante_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Participante já está inscrito neste evento."
            )

    total_inscritos = sum(
        1 for inscricao in inscricoes
        if inscricao["evento_id"] == evento_id
    )

    if total_inscritos >= evento.capacidade:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não existem vagas disponíveis para este evento."
        )

    inscricao = {
        "evento_id": evento_id,
        "participante_id": participante_id
    }
    inscricoes.append(inscricao)

    return {
        "mensagem": "Inscrição realizada com sucesso.",
        "evento_id": evento_id,
        "participante_id": participante_id
    }

def listar_inscritos(evento_id: int, buscar_participante):
    buscar_evento(evento_id)

    participantes_inscritos = []
    for inscricao in inscricoes:
        if inscricao["evento_id"] == evento_id:
            participante = buscar_participante(inscricao["participante_id"])
            if participante:
                participantes_inscritos.append(participante)

    return participantes_inscritos
