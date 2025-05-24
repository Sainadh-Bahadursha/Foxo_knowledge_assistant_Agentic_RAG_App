import streamlit as st
from vectorstore.indexer import FAISSIndexer
from agents.base_agent import FOXOAgent
from tools.life_expectancy import LifeExpectancyTool

# -- Page Setup --
st.set_page_config(page_title="FOXO Knowledge Assistant", layout="wide")
st.title("🧠 FOXO Knowledge Assistant")

st.markdown("""
Welcome to the **FOXO Knowledge Assistant** — your intelligent guide to understanding nutrition, exercise, stress, mental wellness, and more.

This assistant uses internal documents, weather-based food suggestions, a life expectancy tool, and web search fallback — all powered by LangChain's React Agent.

### 💡 Try questions like:
- *How does stress affect mental health?*
- *What food should I eat in Mumbai today?*
- *What is my life expectancy?*
- *Who won the last T20 World Cup?*
""")

st.divider()

@st.cache_resource
def load_agent():
    indexer = FAISSIndexer(persist_dir="vectorstore")
    retriever = indexer.load_index("company_knowledge_index")
    return FOXOAgent(retriever)

agent = load_agent()

# -- Chat State Initialization --
if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_life_inputs" not in st.session_state:
    st.session_state.awaiting_life_inputs = False

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# -- Chat Input --
user_input = st.chat_input("Ask FOXO a question...")

if user_input and not st.session_state.awaiting_life_inputs:
    st.session_state.messages.append({"role": "user", "content": user_input})

    if "life expectancy" in user_input.lower():
        st.session_state.awaiting_life_inputs = True
        st.session_state.pending_question = user_input
        st.rerun()
    else:
        # Add animated typing placeholder
        st.session_state.messages.append({"role": "assistant", "content": "..."})
        st.rerun()

# -- Display Chat History --
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -- Replace Typing Placeholder with Actual Agent Response --
if st.session_state.messages and st.session_state.messages[-1]["content"] == "...":
    last_user_msg = None
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "user":
            last_user_msg = msg["content"]
            break

    if last_user_msg:
        response = agent.ask(last_user_msg)
        st.session_state.messages[-1]["content"] = response
        st.rerun()

# -- Life Expectancy Form --
if st.session_state.awaiting_life_inputs:
    with st.chat_message("assistant"):
        st.markdown("Let's calculate your life expectancy. Please answer the following:")

        with st.form("life_form"):
            age = st.number_input("Your current age", min_value=0, max_value=120, value=30)
            smoker = st.checkbox("Do you smoke?")
            exercise = st.checkbox("Do you exercise regularly?")
            diet = st.checkbox("Do you follow a healthy diet?")
            sleep = st.checkbox("Do you get at least 7 hours of sleep per night?")
            submitted = st.form_submit_button("Calculate")

        if submitted:
            tool = LifeExpectancyTool()
            result = tool.estimate(age, smoker, exercise, diet, sleep)

            st.session_state.messages.append({"role": "assistant", "content": result})
            st.session_state.awaiting_life_inputs = False
            st.session_state.pending_question = None
            st.rerun()
