import os
from pathlib import Path
import streamlit as st

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load .env from common project locations.
_current_file = Path(__file__).resolve()
_dotenv_candidates = [
    _current_file.parents[2] / ".env", 
]
for _dotenv_path in _dotenv_candidates:
    if _dotenv_path.exists():
        load_dotenv(_dotenv_path)
        break


# Chatbot class (same as yours)
class Chatbot:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=api_key,
        )
        self.history = [
            SystemMessage(
                content=(
                    "You are a very Angry AI "
                    "Answer Angry and honestly. If you do not know something, say so."
                )
            )
        ]

    def reply(self, user_input: str) -> str:
        self.history.append(HumanMessage(content=user_input))
        response = self.llm.invoke(self.history)
        content = response.content if isinstance(response.content, str) else str(response.content)
        self.history.append(AIMessage(content=content))
        return content


# ---------------- UI ----------------
st.set_page_config(page_title="Angry AI 🤬", page_icon="🤖")

st.title("🤬 Angry AI Chatbot")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(
        "OPENAI_API_KEY not found. Add it to apps/server/.env "
        "or set it in your environment."
    )
    st.stop()

# session state (important)
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot(api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input box
user_input = st.chat_input("Type your message...")

if user_input:
    # show user msg
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # bot reply
    with st.chat_message("assistant"):
        response = st.session_state.chatbot.reply(user_input)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})