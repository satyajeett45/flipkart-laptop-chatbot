import streamlit as st
from rag_pipeline import answer_query
from query_parser import parse_query

st.set_page_config(page_title="Flipkart Laptop Chatbot", layout="wide")
st.title("💻 Flipkart Laptop Assistant")

# Optional: Clear chat
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input("Ask something about laptops:")

if query:
    parsed = parse_query(query)
    response = answer_query(parsed)

    # Save to session memory
    st.session_state.chat_history.append(("User", query))
    st.session_state.chat_history.append(("Bot", response))

# Display chat
if st.session_state.chat_history:
    st.markdown("### 💬 Chat History")
    for role, msg in st.session_state.chat_history:
        st.markdown(f"**{role}:** {msg}")
