from fastapi import FastAPI
from schems.schemas import CalculationRequest
from tool.calculator import Calc

app = FastAPI()

@app.get("/health")
async def health():
    return {"message": "Success"}

@app.post("/calculate")
async def calculate(request: CalculationRequest):
    try:
        calc = Calc(
            num1=request.num1,
            num2=request.num2,
            operation=request.operation
        )
        result = await calc.execute()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
