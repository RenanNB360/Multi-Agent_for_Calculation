from service.infra.logger import logging
from opentelemetry import trace
import re

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class LLMResponse:

    def __init__(self, content: str):
        self.content = content


class LLMModel:
    def __init__(self, client):
        self.client = client

    async def ainvoke(self, prompt: str) -> LLMResponse:
        with tracer.start_as_current_span("llm.ainvoke"):
            logger.info("Invocando LLM")

            text = await self.client.generate(prompt)
            clean_text = re.sub(r"<thought>.*?</thought>", "", text, flags=re.DOTALL).strip()
            return LLMResponse(clean_text)
