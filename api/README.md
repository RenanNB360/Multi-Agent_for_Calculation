## 1. Papel da pasta `api`

A pasta `api` é responsável por:

- Expor endpoints HTTP usando **FastAPI**
- Validar dados de entrada e saída (Pydantic)
- Orquestrar a execução do grafo de agentes
- Traduzir o estado final do grafo em uma resposta HTTP

Ela **não contém lógica de negócio**, apenas coordena o fluxo entre o cliente e o domínio.

---

## 2. `api/main.py`

Este arquivo é o **entrypoint da API**.

### 2.1 Inicialização

```python
setup_tracing(service_name="artifact-case-api")
app = FastAPI(title="Artifact Case API")
```

- Inicializa observabilidade (tracing)
- Cria a aplicação FastAPI

O logger é carregado antes dos endpoints para registrar todo o ciclo de vida da aplicação.

---

### 2.2 Endpoint `/health`

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

- Endpoint simples de verificação de saúde
- Não depende de nenhuma lógica interna

---

### 2.3 Endpoint `/ask`

```python
@app.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest):
```

Este endpoint recebe uma pergunta e coordena toda a execução.

#### a) Validação de entrada

- O corpo da requisição é validado automaticamente pelo `AskRequest`
- Espera apenas o campo `question`

---

#### b) Criação do estado inicial

```python
initial_state = {
    "user_input": payload.question
}
```

- O grafo opera sobre um dicionário de estado
- A API apenas injeta a pergunta do usuário

---

#### c) Execução do grafo

```python
final_state = await graph.ainvoke(initial_state)
```

- Executa o grafo de forma assíncrona
- Retorna o estado final após todos os nós/agentes

---

#### d) Interpretação do estado final

A API apenas **interpreta chaves conhecidas** no estado:

**Resultado de execução (tool / cálculo)**

```python
if "final_result" in final_state:
```

- Retorna `type="calculation"`
- `content` contém o resultado final

**Resposta direta do LLM**

```python
if "planner_result" in final_state:
```

- Se `action == "answer"`
- Retorna `type="llm_answer"`

**Fallback**

- Caso nenhuma chave esperada exista
- Retorna `type="unknown"`

---

#### e) Tratamento de erros

```python
except Exception as e:
    logger.exception("Erro ao processar requisição")
    raise HTTPException(status_code=500, detail=str(e))
```

- Loga o erro com stack trace
- Retorna HTTP 500 padronizado

---

## 3. `api/utils/factory.py`

Responsável por **criar e montar as dependências** usadas pela API.

### Lógica

- Cria o cliente do LLM
- Encapsula o modelo
- Instancia `PlannerAgent` e `ExecutorAgent`
- Constrói o grafo via `build_graph`

O resultado final é um objeto `graph` pronto para ser usado pela API.

---

## 4. `api/schems/schemas.py`

Define os contratos de entrada e saída.

### AskRequest

- Contém apenas a pergunta do usuário

### AskResponse

- `type`: tipo da resposta
- `content`: resposta principal
- `raw`: estado ou decisão interna (opcional)

---

## 5. Resumo

A pasta `api`:

- Recebe a requisição
- Cria o estado inicial
- Executa o grafo
- Interpreta o resultado
- Retorna um JSON padronizado

Sem conter regras de negócio ou decisões internas.

