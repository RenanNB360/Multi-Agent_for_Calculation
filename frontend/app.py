import streamlit as st
import requests

API_URL = "http://agent-api:8080/ask"

st.set_page_config(
    page_title="Artifact Case Chat",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Artefact Case – Chat")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Digite sua pergunta...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = requests.post(
            API_URL,
            json={"question": user_input},
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        answer = "Não foi possível processar a resposta."

        if data.get("type") == "llm_answer":
            answer = data.get("raw", {}).get("response")

        elif data.get("type") == "calculation":
            answer = data.get("content", {}).get("result")

        if not answer:
            answer = "Resposta vazia retornada pela API."

    except Exception as e:
        answer = f"Erro ao chamar a API: {e}"

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
