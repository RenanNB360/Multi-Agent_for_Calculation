## 1. Papel do Frontend no Projeto

O frontend existe para:

- Permitir que um usuário faça perguntas de forma visual
- Enviar essas perguntas para a API principal (`agent`)
- Exibir a resposta retornada, seja ela do LLM ou de uma tool

Toda a inteligência está na API. O frontend apenas consome.

---

## 2. Conexão com a API

```python
API_URL = "http://agent-api:8080/ask"
```

- Define o endereço da API principal
- O nome `agent-api` é resolvido via Docker Compose
- Toda pergunta do usuário é enviada para essa rota

O frontend não conhece agentes, grafo ou ferramentas — apenas essa URL.

---

## 3. Configuração da Página

```python
st.set_page_config(
    page_title="Artifact Case Chat",
    page_icon="🤖",
    layout="centered",
)
```

- Define título, ícone e layout da aplicação
- Essa configuração roda uma única vez no carregamento

Em seguida, o título principal da interface é exibido.

---

## 4. Controle de Estado da Conversa

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

- Usa o `session_state` do Streamlit para manter o histórico
- Sem isso, a conversa seria perdida a cada interação

Cada mensagem é armazenada com:

- `role`: user ou assistant
- `content`: texto exibido no chat

---

## 5. Renderização do Histórico

```python
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
```

- Reexibe todo o histórico da conversa
- Garante que o chat pareça contínuo para o usuário

---

## 6. Entrada do Usuário

```python
user_input = st.chat_input("Digite sua pergunta...")
```

- Campo de input no formato de chat
- Retorna valor apenas quando o usuário envia a mensagem

Quando há entrada, o fluxo da conversa começa.

---

## 7. Envio da Pergunta para a API

Após o usuário enviar a pergunta:

- A mensagem é adicionada ao histórico
- A pergunta é exibida imediatamente no chat
- A API é chamada via `requests.post`

```python
response = requests.post(
    API_URL,
    json={"question": user_input},
    timeout=60,
)
```

O frontend apenas envia o texto — nenhuma interpretação acontece aqui.

---

## 8. Tratamento da Resposta

O frontend interpreta a resposta apenas pelo campo `type`:

- **`llm_answer`** → resposta direta do modelo
- **`calculation`** → resultado retornado por uma tool

Com base nisso, o texto final exibido é escolhido.

Caso a API retorne algo inesperado ou vazio, mensagens de fallback são usadas para evitar respostas quebradas na UI.

---

## 9. Tratamento de Erros

```python
except Exception as e:
    answer = f"Erro ao chamar a API: {e}"
```

- Qualquer erro de rede ou timeout é capturado
- O erro é exibido de forma clara para o usuário

Isso evita que a interface quebre silenciosamente.

---

## 10. Exibição da Resposta

Por fim:

- A resposta é adicionada ao histórico
- O texto é renderizado como mensagem do assistente

Isso fecha o ciclo da interação.

---

## 11. Resumo da Lógica

O frontend:

- Mantém o estado da conversa
- Envia perguntas para a API
- Interpreta apenas o tipo da resposta
- Exibe o resultado para o usuário

Nada mais que isso — simples, previsível e fáci