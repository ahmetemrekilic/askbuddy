from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import streamlit as st


llm = ChatMistralAI(model="mistral-small-2506")

st.title("Chat Bot 🤖")
st.markdown("Japanese-optimized AI chatbot 🇯🇵")

# 🔥 Japonca optimize system prompt
system_prompt = SystemMessage(content="""
You are a professional Japanese assistant.

- Always respond in fluent, natural Japanese
- Prefer polite form (です・ます)
- Use casual tone only if the user is casual
- Keep answers clear and concise
- If explaining technical topics, use simple Japanese

Always respond in natural Japanese.
Use polite Japanese (敬語) when appropriate.
Make responses sound natural and human-like, not robotic.
If the user writes in English, still respond in Japanese unless explicitly asked otherwise.
""")

if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# geçmiş mesajları göster
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        st.chat_message("user").markdown(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("ai").markdown(message.content)

query = st.chat_input("Ask anything ?")


if query:
    human_msg = HumanMessage(content=query)
    st.session_state.messages.append(human_msg)
    st.chat_message("user").markdown(query)

    # 🔥 tüm conversation + system prompt modele gidiyor
    res = llm.invoke(st.session_state.messages)

    ai_msg = AIMessage(content=res.content)
    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append(ai_msg)