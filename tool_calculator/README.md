## Visão geral da lógica

O serviço expõe uma API HTTP usando FastAPI com dois endpoints principais:

- Um endpoint de saúde (`/health`), usado para verificação de disponibilidade do serviço
- Um endpoint de cálculo (`/calculate`), que recebe os dados da operação e retorna o resultado

Toda a lógica matemática fica encapsulada em uma classe dedicada, mantendo o código simples, previsível e fácil de testar.

## main.py – Camada de API

O arquivo `main.py` funciona apenas como a **porta de entrada HTTP** do serviço.

Ele recebe uma requisição com:
- dois números (`num1` e `num2`)
- um operador matemático (`operation`)

Esses dados são validados automaticamente pelo Pydantic e então repassados para a camada de cálculo. O endpoint não toma decisões nem executa lógica matemática diretamente — ele apenas orquestra a chamada e devolve a resposta.

Em caso de erro (como uma operação inválida ou divisão por zero), o serviço retorna a mensagem de erro de forma simples, sem tentar mascarar o problema.

## calculator.py – Lógica de negócio

A classe `Calc` concentra toda a lógica matemática do serviço.

Ela suporta exatamente **quatro operações**:
- Soma (`+`)
- Subtração (`-`)
- Multiplicação (`*`)
- Divisão (`/`)

Cada operação é tratada de forma explícita, sem atalhos ou abstrações desnecessárias. No caso da divisão, existe uma validação clara para evitar divisão por zero, garantindo que erros matemáticos não passem despercebidos.

Mesmo sendo uma lógica simples, ela foi isolada em uma classe própria para facilitar reutilização, testes unitários e futuras extensões.

## schemas.py – Contrato de entrada

O arquivo `schemas.py` define o **contrato da requisição** usando Pydantic.

Isso garante que:
- Os dados recebidos pela API tenham o tipo correto
- Erros de entrada sejam tratados automaticamente antes de chegar à lógica de cálculo

Essa validação evita que o serviço execute operações com dados inconsistentes e mantém a API previsível.

## Papel do serviço na arquitetura

Este serviço existe para cumprir uma função bem específica:

- Executar cálculos matemáticos de forma confiável
- Ser chamado por outros serviços via HTTP
- Evitar que LLMs ou agentes tentem resolver operações matemáticas por conta própria

Na arquitetura geral, ele atua como uma **ferramenta externa**, garantindo separação de responsabilidades e resultados consistentes.