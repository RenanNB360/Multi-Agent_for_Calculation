import httpx
import os
from service.infra.logger import logging
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

async def call_calculator(num1: float, num2: float, operation: str) -> dict:
    
    calc_api_url = os.getenv("CALCULATOR_API_URL", "http://calc-api:8500/calculate")

    payload = {
        "num1": num1,
        "num2": num2,
        "operation": operation,
    }

    logger.info("Chamando API Calculadora via HTTP: %s", calc_api_url)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(calc_api_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "result" in data:
                return {
                    "ok": True,
                    "result": data["result"],
                }
            return {"ok": False, "error": data.get("error", "Resposta desconhecida")}
            
    except Exception as e:
        logger.error("Erro ao chamar API Calculadora: %s", str(e))
        return {"ok": False, "error": str(e)}