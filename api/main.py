from fastapi import FastAPI, HTTPException
from api.schems.schemas import AskRequest, AskResponse

from service.infra.logger import logging
from service.infra.observability import setup_tracing

from api.utils.factory import graph

logger = logging.getLogger(__name__)

setup_tracing(service_name="artifact-case-api")

app = FastAPI(title="Artifact Case API")


logger.info("Inicializando dependências da aplicação")


logger.info("Graph LangGraph compilado com sucesso")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest):

    try:
        logger.info("Pergunta recebida | question=%s", payload.question)

        initial_state = {
            "user_input": payload.question
        }

        final_state = await graph.ainvoke(initial_state)

        if "final_result" in final_state:
            content_data = final_state.pop("final_result") 
            return AskResponse(
                type="calculation",
                content=content_data,
                raw=final_state,
            )

        if "planner_result" in final_state:
            planner_result = final_state["planner_result"]

            if planner_result.get("action") == "answer":
                return AskResponse(
                    type="llm_answer",
                    content=planner_result.get("answer"),
                    raw=planner_result,
                )

        return AskResponse(
            type="unknown",
            content="Não foi possível determinar a resposta",
            raw=final_state,
        )

    except Exception as e:
        logger.exception("Erro ao processar requisição")
        raise HTTPException(status_code=500, detail=str(e))
