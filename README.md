# API RESTful de Eventos Acadêmicos

Projeto desenvolvido em Python com FastAPI para gerenciamento de eventos acadêmicos, participantes e inscrições.

## Funcionalidades

A API permite:

- Cadastrar, listar, consultar, atualizar e excluir eventos;
- Cadastrar, listar, consultar, atualizar e excluir participantes;
- Inscrever participantes em eventos;
- Consultar participantes inscritos;
- Validar dados com Pydantic;
- Controlar capacidade dos eventos;
- Impedir inscrições duplicadas;
- Retornar códigos HTTP apropriados;
- Documentar e testar a API pelo Swagger.

## Estrutura do projeto

```text
api_eventos_fastapi/
│
├── main.py
├── requirements.txt
├── README.md
│
├── controller/
│   ├── __init__.py
│   ├── evento_controller.py
│   └── participante_controller.py
│
├── model/
│   ├── __init__.py
│   ├── evento.py
│   └── participante.py
│
└── service/
    ├── __init__.py
    ├── evento_service.py
    └── participante_service.py
```

## Instalação

Recomenda-se utilizar um ambiente virtual.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Execução

Na pasta do projeto:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Principais rotas

### Eventos

| Método | Rota | Função |
|---|---|---|
| POST | `/eventos` | Cadastrar evento |
| GET | `/eventos` | Listar eventos |
| GET | `/eventos/{id}` | Consultar evento |
| PUT | `/eventos/{id}` | Atualizar evento |
| DELETE | `/eventos/{id}` | Excluir evento |
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | Realizar inscrição |
| GET | `/eventos/{evento_id}/inscricoes` | Listar inscritos |

### Participantes

| Método | Rota | Função |
|---|---|---|
| POST | `/participantes` | Cadastrar participante |
| GET | `/participantes` | Listar participantes |
| GET | `/participantes/{id}` | Consultar participante |
| PUT | `/participantes/{id}` | Atualizar participante |
| DELETE | `/participantes/{id}` | Excluir participante |

## Exemplo: cadastrar evento

Requisição:

```json
{
  "titulo": "Workshop de Python",
  "descricao": "Introdução ao desenvolvimento com Python e FastAPI.",
  "data": "2026-10-15",
  "horario": "19:00:00",
  "local": "Laboratório 2",
  "capacidade": 30,
  "categoria": "Workshop"
}
```

Resposta `201 Created`:

```json
{
  "titulo": "Workshop de Python",
  "descricao": "Introdução ao desenvolvimento com Python e FastAPI.",
  "data": "2026-10-15",
  "horario": "19:00:00",
  "local": "Laboratório 2",
  "capacidade": 30,
  "categoria": "Workshop",
  "id": 1
}
```

## Exemplo: cadastrar participante

Requisição:

```json
{
  "nome": "João da Silva",
  "email": "joao@email.com",
  "curso": "Análise e Desenvolvimento de Sistemas"
}
```

Resposta `201 Created`:

```json
{
  "nome": "João da Silva",
  "email": "joao@email.com",
  "curso": "Análise e Desenvolvimento de Sistemas",
  "id": 1
}
```

## Exemplo: realizar inscrição

```text
POST /eventos/1/inscricoes/1
```

Resposta:

```json
{
  "mensagem": "Inscrição realizada com sucesso.",
  "evento_id": 1,
  "participante_id": 1
}
```

## Exemplos de erros

Evento inexistente:

```json
{
  "detail": "Evento não encontrado."
}
```

Participante inexistente:

```json
{
  "detail": "Participante não encontrado."
}
```

Participante já inscrito:

```json
{
  "detail": "Participante já está inscrito neste evento."
}
```

Evento sem vagas:

```json
{
  "detail": "Não existem vagas disponíveis para este evento."
}
```

E-mail inválido ou outro erro de validação:

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address"
    }
  ]
}
```

## Códigos HTTP utilizados

- `200 OK`: consultas e atualizações realizadas com sucesso;
- `201 Created`: criação de eventos, participantes e inscrições;
- `204 No Content`: exclusões realizadas com sucesso;
- `404 Not Found`: recurso não encontrado;
- `409 Conflict`: conflito de negócio, como inscrição duplicada ou evento sem vagas;
- `422 Unprocessable Entity`: dados enviados não passam pela validação do Pydantic.

## Arquitetura MVC

### Model

Os arquivos dentro de `model/` representam os dados e suas validações utilizando Pydantic.

### Controller

Os arquivos dentro de `controller/` definem as rotas HTTP e recebem as requisições.

### Service

Os arquivos dentro de `service/` concentram as regras de negócio, como:

- verificar existência de evento;
- verificar existência de participante;
- impedir inscrição duplicada;
- verificar capacidade do evento;
- impedir e-mails duplicados.

## Armazenamento

Os dados são armazenados em listas Python na memória, conforme permitido pela atividade. Portanto, os dados são perdidos quando a aplicação é encerrada.

## Testes no Swagger

Depois de executar a aplicação, acesse:

```text
http://127.0.0.1:8000/docs
```

Sugestão de sequência para demonstração:

1. Criar um evento;
2. Criar um participante;
3. Consultar o evento;
4. Consultar o participante;
5. Realizar a inscrição;
6. Consultar as inscrições do evento;
7. Tentar realizar a mesma inscrição novamente;
8. Atualizar evento ou participante;
9. Excluir evento ou participante;
10. Testar dados inválidos, como e-mail incorreto e capacidade igual a zero.
