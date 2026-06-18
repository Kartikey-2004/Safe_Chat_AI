import streamlit as st
from main import ChatBot

st.set_page_config(page_title="Secure AI Chat", page_icon="🤖", layout="centered")

st.title("🤖 Secure AI Chatbot")
st.markdown("Equipped with Presidio PII Masking and Smart Model Routing.")

if "bot" not in st.session_state:
    st.session_state.bot = ChatBot()

if "ui_messages" not in st.session_state:
    st.session_state.ui_messages = []

for msg in st.session_state.ui_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "metrics" in msg:
            st.caption(msg["metrics"])

if user_query := st.chat_input("Type your message here..."):

    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.ui_messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = st.session_state.bot.smart_chat(user_query)

                if result["safe_query"] != user_query:
                    st.info(
                        "🛡️ **Guardrail active:** PII was detected and masked before reaching the model."
                    )

                answer = result["answer"]
                metrics_text = (
                    f"**Model:** `{result['model_used']}` | "
                    f"**Task:** `{result['detected_task']}` | "
                    f"**Model latency:** `{result['latency_sec']}s` | "
                    f"**Total latency:** `{result['total_latency_sec']}s` | "
                    f"**Cost:** `{result['cost_usd']}`"
                )

                st.markdown(answer)
                st.caption(metrics_text)

                st.session_state.ui_messages.append(
                    {"role": "assistant", "content": answer, "metrics": metrics_text}
                )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
