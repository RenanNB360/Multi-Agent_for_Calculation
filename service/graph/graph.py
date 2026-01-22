from langgraph.graph import StateGraph, END
from typing import Dict, Any

from service.graph.nodes import planner_node, executor_node
from service.infra.logger import logging

logger = logging.getLogger(__name__)


def build_graph(planner, executor):
    graph = StateGraph(Dict[str, Any])

    async def planner_wrapper(state: Dict[str, Any]) -> Dict[str, Any]:
        return await planner_node(state, planner)

    async def executor_wrapper(state: Dict[str, Any]) -> Dict[str, Any]:
        return await executor_node(state, executor)

    graph.add_node("planner", planner_wrapper)
    graph.add_node("executor", executor_wrapper)

    graph.set_entry_point("planner")

    graph.add_conditional_edges(
        "planner",
        lambda state: (
            "executor"
            if state.get("planner_result", {}).get("action") == "calculate"
            else END
        ),
        {
            "executor": "executor",
            END: END,
        },
    )

    graph.add_edge("executor", END)

    return graph.compile()
