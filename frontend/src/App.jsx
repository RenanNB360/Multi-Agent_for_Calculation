import { useState } from "react";

const API_URL = "http://localhost:8080/ask";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", content: input };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000);

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userMessage.content }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`Erro HTTP ${response.status}`);
      }

      const data = await response.json();

      let answer = "Não foi possível processar a resposta.";

      if (data.type === "llm_answer") {
        answer = data.raw?.response;
      } else if (data.type === "calculation") {
        answer = data.content?.result;
      }

      if (!answer) {
        answer = "Resposta vazia retornada pela API.";
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: answer },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            error.name === "AbortError"
              ? "⏱️ A requisição demorou demais."
              : `Erro ao chamar a API: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2>🤖 Artifact Case – Chat</h2>

      <div style={styles.chatBox}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
              backgroundColor:
                msg.role === "user" ? "#DCF8C6" : "#F1F0F0",
            }}
          >
            {msg.content}
          </div>
        ))}

        {loading && (
          <div style={{ fontSize: "12px", color: "#666" }}>
            🤖 Pensando...
          </div>
        )}
      </div>

      <div style={styles.inputBox}>
        <input
          type="text"
          placeholder="Digite sua pergunta..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={loading}
          style={styles.input}
        />
        <button onClick={sendMessage} disabled={loading} style={styles.button}>
          Enviar
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "600px",
    margin: "0 auto",
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    fontFamily: "Arial, sans-serif",
  },
  chatBox: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    overflowY: "auto",
    marginBottom: "12px",
    padding: "10px",
    border: "1px solid #ddd",
    borderRadius: "6px",
  },
  message: {
    padding: "10px 14px",
    borderRadius: "10px",
    maxWidth: "80%",
    fontSize: "14px",
    lineHeight: "1.4",
  },
  inputBox: {
    display: "flex",
    gap: "8px",
  },
  input: {
    flex: 1,
    padding: "10px",
    fontSize: "14px",
  },
  button: {
    padding: "10px 16px",
    cursor: "pointer",
  },
};
