from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from agents.tool_router import get_tools
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

class FOXOAgent:
    def __init__(self, retriever):
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0
        )

        tools = get_tools(retriever)

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
            memory=self.memory
        )

    def ask(self, query: str) -> str:
        try:
            result = self.agent.invoke({"input": query})
            return result["output"]
        except Exception as e:
            return f"❌ Agent failed: {str(e)}"
