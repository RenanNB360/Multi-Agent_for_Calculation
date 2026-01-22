from pydantic import BaseModel

class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str