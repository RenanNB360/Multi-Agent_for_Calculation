import httpx
from service.infra.logger import logging
from opentelemetry import trace
import os

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class OllamaClient:
    def __init__(
        self,
        base_url: str | None = None,
        model: str = "qwen3:14b",
        timeout: int = 60,
    ):
        self.base_url = base_url or os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.model = model
        self.timeout = timeout

    async def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        }

        with tracer.start_as_current_span("ollama.generate"):
            logger.info("Chamando Ollama | model=%s", self.model)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

                data = response.json()

                return data.get("response", "")
