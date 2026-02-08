import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Investor With Multiple Agents", page_icon="⚖️", layout="wide")

st.title("AI Investor With Multiple Agents")
st.markdown("""
This system simulates a high-level investment meeting with three conflicting perspectives:
1.  **The Optimistic**: Searches for growth and catalysts.
2.  **The Pessimistic**: Digs for risks and pitfalls.
3.  **The Analytical Researcher**: Analyzes hard market data and trends.
""")

BACKEND_URL = "http://127.0.0.1:550/ask" 

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.title("System Status")
st.sidebar.info(f"**Architecture:** Parallel Investment Committee\n\n**Thread ID:** `{st.session_state.thread_id}`")

if st.sidebar.button("Reset Session"):
    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Enter stock symbol (e.g., TSLA, AAPL, NVDA)..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("The Committee is debating (Optimistic vs Pessimistic vs Analytical Researcher)..."):
            try:
                response = requests.post(
                    BACKEND_URL, 
                    params={"request": prompt}, 
                    timeout=150
                )
                
                if response.status_code == 200:
                    api_data = response.json()
                    final_verdict = api_data.get("messages", "Error: No verdict found.")
                    
                    tab1, tab2 = st.tabs(["🎯 Final Verdict", "🔍 Inside the Debate"])
                    
                    with tab1:
                        st.markdown("### The Agents Decision")
                        st.markdown(final_verdict)
                    
                    with tab2:
                        st.info("The agents perform parallel deep-dives into recent news and market stats to reach this consensus.")
                        st.write("Current analysis thread focus: " + prompt)
                    
                    st.session_state.messages.append({"role": "assistant", "content": final_verdict})
                
                else:
                    st.error(f"Backend Error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                st.error("The analysts took too long to respond. Try again.")
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")

st.divider()
st.caption("UI Connected to FastAPI Backend | Monitoring via Langfuse (on Backend)")