from fastapi import FastAPI
from controller.evento_controller import router as evento_router
from controller.participante_controller import router as participante_router

app = FastAPI(
    title="API de Eventos Acadêmicos",
    description="API RESTful para gerenciamento de eventos, participantes e inscrições.",
    version="1.0.0"
)

app.include_router(evento_router)
app.include_router(participante_router)

@app.get("/", tags=["Sistema"])
def inicio():
    return {
        "mensagem": "API de Eventos Acadêmicos funcionando!",
        "documentacao": "/docs"
    }
