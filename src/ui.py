from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
import gradio as gr
from langgraph.prebuilt.chat_agent_executor import AgentState

from src.agent import socrates_buddy


def predict(message, history):
    def add_history():
        for msg in history:
            if msg["role"] == "user":
                history_langchain_format.append(HumanMessage(msg["content"]))
            elif msg["role"] == "assistant":
                history_langchain_format.append(AIMessage(msg["content"]))

    def add_last_human_message():
        history_langchain_format.append(HumanMessage(message))

    history_langchain_format = []
    add_history()
    add_last_human_message()

    output = socrates_buddy.invoke(AgentState(messages=history_langchain_format))
    return output["messages"][-1].content


demo = gr.ChatInterface(
    predict,
    type="messages",
    title="SoCraTes Buddy",
    description="Craft your ideal SoCraTes schedule for the day!",
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
    )
