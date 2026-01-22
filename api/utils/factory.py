from service.infra.ollama_client import OllamaClient
from service.infra.llm_model import LLMModel
from service.agents.planner_agent import PlannerAgent
from service.agents.executor_agent import ExecutorAgent
from service.graph.graph import build_graph


ollama_client = OllamaClient()
llm = LLMModel(ollama_client)

planner = PlannerAgent(model=llm)
executor = ExecutorAgent(model=llm)

graph = build_graph(
    planner=planner,
    executor=executor,
)
