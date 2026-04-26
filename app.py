from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import streamlit as st


llm = ChatMistralAI(model="mistral-small-2506")

st.title("Chat Bot 🤖")
st.markdown("Japanese-optimized AI chatbot 🇯🇵")


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

You are a multilingual assistant specialized in Japanese, English, and Turkish.

Core Behavior:
- Detect the user's language automatically.
- Reply in the same language.
- If the user writes in Japanese, keep responses natural and simple (JLPT N3–N2 level).
- If needed, add brief English explanations for difficult Japanese phrases.

Adaptive Behavior:
- If the user mixes languages, respond in the dominant one.
- If the user is unclear, ask a clarification question.
- If the user asks for translation, provide clean translations without extra text.

Learning Support:
- When the user writes in Japanese, occasionally:
  - Add furigana for difficult kanji (optional)
  - Give short vocabulary hints

Consistency:
- Do not randomly switch languages.
- Maintain the conversation language unless the user changes it.

Fallback Rule:
- If a language is not supported well, respond in English.

Error Handling:
- If unsure about the language, ask:
  "Which language would you like me to respond in?"

""")

if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]


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


    res = llm.invoke(st.session_state.messages)

    ai_msg = AIMessage(content=res.content)
    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append(ai_msg)