from typing import Dict, Any

from service.infra.logger import logging
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


async def planner_node(state: Dict[str, Any], planner) -> Dict[str, Any]:

    with tracer.start_as_current_span("graph.node.planner"):
        user_input = state.get("user_input")

        logger.info("Planner node iniciado")

        result = await planner.run(user_input)

        logger.info("Planner node finalizado")

        return {
            **state,
            "planner_result": result,
        }


async def executor_node(state: Dict[str, Any], executor) -> Dict[str, Any]:

    with tracer.start_as_current_span("graph.node.executor"):
        planner_result = state.get("planner_result", {})

        logger.info("Executor node iniciado")

        result = await executor.run(
            num1=planner_result["num1"],
            num2=planner_result["num2"],
            operation=planner_result["operator"],
        )

        logger.info("Executor node finalizado")

        return {
            **state,
            "final_result": result,
        }
