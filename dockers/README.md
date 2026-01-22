### `agent/dockerfile`

Esse dockerfile é responsável por criar a imagem da aplicação FastAPI que orquestra os agentes, o grafo de decisão e a comunicação com ferramentas externas.

Ele é o container central do projeto — frontend e tools dependem dele para funcionar. Define que o container executa uma **aplicação ASGI** usando Uvicorn
expondo a porta 8080. Ele puxa todos os arquivos do proejto, exceto os diretorios **dockers, frontend e tool_calculator**.

```bash
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

### `frontend/dockerfile`

O Dockerfile **frontend** existe para subir a **interface gráfica** da aplicação.

Para este container é exposta a porta 8501.Ele puxa todos os arquivos presentes no diretorio **frontend**.

```bash
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

---

### `tool_calculator/dockerfile`

O Dockerfile **tool_calculator** representa uma **ferramenta externa independente** com FastAPI. 

Esse container existe para ser chamado pelo Executor Agent quando uma execução concreta é necessária. Para este container é exposta a porta 8501.
Ele puxa todos os arquivos do diretorio **tool_calculator**.

```bash
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8500"]
```