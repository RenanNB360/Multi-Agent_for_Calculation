from pathlib import Path
from typing import Dict, Any
import re
import yaml
from typing import Tuple

from service.infra.logger import logging
from opentelemetry import trace

from service.mcp_client.client import call_calculator

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class ExecutorAgent:
    def __init__(self, model):
        self.model = model

        with tracer.start_as_current_span("executor.load_prompt"):
            self.template, self.version = self._load_prompt()
            logger.info("ExecutorAgent usando prompt versão %s", self.version)

        logger.info("ExecutorAgent inicializado")

    def _load_prompt(self) -> Tuple[str, str]:

        base_path = Path(__file__).parent.parent / "prompts"
        prompt_files = list(base_path.glob("v*_executor.yaml"))

        if not prompt_files:
            logger.error("Nenhum prompt do Executor encontrado em %s", base_path)
            return "A resposta para sua pergunta é {result}.", "unknown"

        def get_version_number(path: Path) -> int:
            match = re.search(r"v(\d+)", path.name)
            return int(match.group(1)) if match else 0

        prompt_files.sort(key=get_version_number, reverse=True)

        for file in prompt_files:
            version = f"v{get_version_number(file)}"
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                template = data.get("template")
                if not template:
                    raise ValueError("Campo 'template' não encontrado")

                logger.info(
                    "Prompt do Executor carregado com sucesso | versão=%s arquivo=%s",
                    version,
                    file.name,
                )
                return template, version

            except Exception as e:
                logger.warning(
                    "Erro ao carregar prompt %s, tentando versão anterior | error=%s",
                    file.name,
                    str(e),
                )

        logger.error("Nenhum prompt válido do Executor encontrado")
        return "A resposta para sua pergunta é {result}.", "unknown"


    async def _format_response(self, result: Any) -> str:
        prompt_final = self.template.format(result=result)

        with tracer.start_as_current_span("executor.llm_call"):
            logger.info("Executor chamando LLM para formatar resposta")
            response = await self.model.ainvoke(prompt_final)
            
            text = response.content if hasattr(response, "content") else str(response)

            cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

        return cleaned_text

    async def run(self, num1: float, num2: float, operation: str) -> Dict:
        with tracer.start_as_current_span("executor.run"):
            logger.info(
                "Executor chamando calculadora | num1=%s num2=%s op=%s",
                num1,
                num2,
                operation,
            )

            calc_result = await call_calculator(
                num1=num1,
                num2=num2,
                operation=operation,
            )

            if not calc_result.get("ok"):
                logger.warning(
                    "Falha ao executar cálculo: %s",
                    calc_result.get("error"),
                )
                return calc_result

            try:
                formatted = await self._format_response(
                    calc_result.get("result")
                )

                logger.info("Resposta formatada com sucesso pelo Executor")

                return {
                    "ok": True,
                    "result": formatted,
                }

            except Exception as e:
                logger.exception("Erro ao formatar resposta no Executor")
                return {
                    "ok": False,
                    "error": str(e),
                }
