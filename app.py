import streamlit as st
import requests

st.title("📅 TailorTalk – AI Appointment Scheduler")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask me to check or book a calendar slot...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        res = requests.post("http://localhost:8000/chat", json={"message": user_input})
        st.write("DEBUG status code:", res.status_code)
        st.write("DEBUG response text:", res.text)

        if res.status_code == 200:
            response = res.json().get("response")
        else:
            response = f"❌ Backend Error: {res.status_code} – {res.text}"

    except Exception as e:
        response = f"❌ Request failed: {e}"

    st.session_state.messages.append({"role": "assistant", "content": response})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
