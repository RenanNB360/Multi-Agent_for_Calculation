## 1. Papel do Frontend no Projeto

O frontend existe para:

- Permitir que o usuário faça perguntas por meio de uma interface web
- Enviar essas perguntas para a API principal (`agent`)
- Exibir a resposta retornada, seja ela gerada pelo LLM ou por uma tool

Toda a inteligência do sistema está concentrada na API.  
O frontend atua apenas como **camada de apresentação e consumo**, sem regras de negócio.

---

## 2. Conexão com a API

```ts
const API_URL = "http://agent-api:8080/ask";
```

- Define o endereço da API principal
- O nome `agent-api` é resolvido automaticamente via Docker Compose
- Toda pergunta do usuário é enviada para essa rota
- O frontend não conhece agentes, grafos ou ferramentas internas — apenas consome essa URL.

---

## 3. Stack do Frontend

O frontend foi desenvolvido utilizando:

- React
- Vite
- JavaScript
- Fetch API
- Docker

A aplicação roda localmente em:

```
http://localhost:5173
```

Quando executada via Docker, essa porta é exposta pelo container.

---

## 4. Estrutura Geral da Aplicação

A aplicação segue um fluxo simples:

1. O usuário digita uma pergunta
2. A pergunta é enviada para a API
3. A resposta é recebida
4. O histórico da conversa é atualizado
5. A interface é re-renderizada

Tudo acontece sem recarregar a página.

---

## 5. Controle de Estado da Conversa

O histórico da conversa é mantido no estado do React:

```js
const [messages, setMessages] = useState([]);
```

Cada mensagem segue o formato:

```js
{
  role: "user" | "assistant",
  content: string
}
```

Isso garante que:

- O histórico não seja perdido durante a sessão
- O chat seja renderizado de forma contínua
- O estado fique previsível e fácil de depurar

---

## 6. Renderização do Histórico

O histórico é percorrido e renderizado dinamicamente:

```jsx
messages.map((msg, index) => (
  <ChatMessage key={index} role={msg.role} content={msg.content} />
));
```

Cada mensagem é exibida de acordo com seu papel:

- `user` → mensagem do usuário
- `assistant` → resposta da API

---

## 7. Entrada do Usuário

O input principal permite que o usuário envie perguntas:

```jsx
<input
  value={input}
  onChange={(e) => setInput(e.target.value)}
  placeholder="Digite sua pergunta..."
/>
```

Ao enviar a mensagem:

- O texto é adicionado imediatamente ao histórico
- A chamada para a API é iniciada

---

## 8. Envio da Pergunta para a API

A comunicação com o backend ocorre via fetch:

```js
const response = await fetch(API_URL, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    question: userInput,
  }),
});
```

O frontend envia apenas o texto da pergunta, sem qualquer interpretação.

---

## 9. Tratamento da Resposta

A resposta da API é interpretada pelo campo `type`:

- `llm_answer` → resposta direta do modelo
- `calculation` → resultado retornado por uma tool

Com base nisso, o texto exibido ao usuário é definido.

Caso a resposta seja inválida ou inesperada, mensagens de fallback são utilizadas para evitar falhas na interface.

---

## 10. Tratamento de Erros

Erros de rede, timeout ou falha da API são tratados com try/catch:

```js
catch (error) {
  setMessages((prev) => [
    ...prev,
    { role: "assistant", content: "Erro ao chamar a API." },
  ]);
}
```

Isso garante que:

- A interface não quebre
- O usuário receba feedback claro
- O estado do chat permaneça consistente

---

## 11. Resumo da Lógica do Frontend

O frontend:

- Mantém o estado da conversa
- Envia perguntas para a API
- Interpreta apenas o tipo da resposta
- Renderiza o histórico de mensagens
- Trata erros de forma controlada

Nada mais que isso — simples, previsível e desacoplado.

---

## 12. Observação Importante

Toda a lógica de decisão, agentes, ferramentas e orquestração está localizada na API (`agent`).

O frontend não possui regras de negócio e pode ser facilmente substituído por outra interface (CLI, mobile, etc.).
