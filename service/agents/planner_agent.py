import json
import re
import yaml
import asyncio
from service.infra.logger import logging

from pathlib import Path
from typing import Any, Dict

from opentelemetry import trace

logger = logging.getLogger(__name__)

tracer = trace.get_tracer(__name__)


class PlannerAgent:
    def __init__(self, model):
        self.model = model

        with tracer.start_as_current_span("planner.load_prompt"):
            self.template, self.version = self._load_prompt()

        logger.info("PlannerAgent inicializado com prompt versão %s", self.version)

    def _load_prompt(self) -> tuple[str, str]:
        base_path = Path(__file__).parent.parent / "prompts"
        prompt_files = list(base_path.glob("v*_planner.yaml"))

        if not prompt_files:
            logger.error("Nenhum prompt do Planner encontrado em %s", base_path)
            return "{user_input}", "unknown"

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
                    "Prompt do Planner carregado com sucesso | versão=%s arquivo=%s",
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

        logger.error("Nenhum prompt válido do Planner encontrado")
        return "{user_input}", "unknown"


    async def execute_llm(self, user_input: str) -> str:

        prompt_final = self.template.format(user_input=user_input)

        with tracer.start_as_current_span("planner.llm_call"):
            logger.info("Executando chamada ao LLM no PlannerAgent")

            response = await self.model.ainvoke(prompt_final)

        return response.content if hasattr(response, "content") else str(response)

    async def run(self, user_input: str) -> Dict[str, Any]:

        with tracer.start_as_current_span("planner.run"):
            try:
                raw_response = await self.execute_llm(user_input)

                parsed = self._parse_json_response(raw_response)

                logger.info("PlannerAgent executado com sucesso")

                return parsed

            except Exception as e:
                logger.exception(
                    f"Erro no PlannerAgent (versão {self.version}): {str(e)}"
                )
                return {
                    "ok": False,
                    "error": str(e),
                    "version": self.version,
                }

    @staticmethod
    def _parse_json_response(text: str) -> Dict[str, Any]:
        
        text_no_think = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

        start_idx = text_no_think.find('{')
        end_idx = text_no_think.rfind('}')

        if start_idx == -1 or end_idx == -1:
            logger.error(f"JSON não encontrado na resposta: {text}")
            raise ValueError("O LLM não retornou um objeto JSON válido.")

        json_str = text_no_think[start_idx:end_idx + 1]

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            try:
                json_str_fixed = json_str.replace('\n', ' ').replace('\r', '')
                return json.loads(json_str_fixed)
            except Exception as e:
                logger.error(f"Falha crítica no parse. Texto extraído: {json_str}")
                raise ValueError("Erro ao decodificar o JSON do modelo.") from e