from fastapi import HTTPException, status
from model.participante import Participante, ParticipanteCreate, ParticipanteUpdate

participantes: list[Participante] = []
proximo_id = 1

def cadastrar_participante(dados: ParticipanteCreate) -> Participante:
    global proximo_id

    email = str(dados.email).lower()

    for participante in participantes:
        if str(participante.email).lower() == email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um participante cadastrado com este e-mail."
            )

    participante = Participante(id=proximo_id, **dados.model_dump())
    participantes.append(participante)
    proximo_id += 1

    return participante

def listar_participantes() -> list[Participante]:
    return participantes

def buscar_participante(participante_id: int) -> Participante | None:
    for participante in participantes:
        if participante.id == participante_id:
            return participante
    return None

def buscar_participante_ou_erro(participante_id: int) -> Participante:
    participante = buscar_participante(participante_id)

    if participante is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante não encontrado."
        )

    return participante

def atualizar_participante(
    participante_id: int,
    dados: ParticipanteUpdate
) -> Participante:
    participante = buscar_participante_ou_erro(participante_id)

    novo_email = str(dados.email).lower()

    for outro in participantes:
        if outro.id != participante_id and str(outro.email).lower() == novo_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe outro participante com este e-mail."
            )

    for campo, valor in dados.model_dump().items():
        setattr(participante, campo, valor)

    return participante

def excluir_participante(participante_id: int):
    participante = buscar_participante_ou_erro(participante_id)
    participantes.remove(participante)
