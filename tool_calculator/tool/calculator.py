
class Calc:
    def __init__(self, num1: float, num2: float, operation: str):
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    async def execute(self):
        if self.operation == '+':
            return self.num1 + self.num2
        elif self.operation == '-':
            return self.num1 - self.num2
        elif self.operation == '*':
            return self.num1 * self.num2
        elif self.operation == '/':
            if self.num2 != 0:
                return self.num1 / self.num2
            else:
                raise ValueError("Divisão por zero não permitida")