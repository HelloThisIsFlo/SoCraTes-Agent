from langchain_core.messages import HumanMessage
from langgraph.constants import END, START
from langgraph.graph.message import MessagesState
from langgraph.graph.state import StateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from src.config import get_small_model


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_react_agent(
    model=get_small_model(),
    tools=[get_weather],
    prompt="You are a helpful assistant",
)


def sandbox_agent(state: MessagesState) -> MessagesState:
    resp = agent.invoke(state)
    return {"messages": resp["messages"]}


graph_builder = (
    StateGraph(MessagesState)
    .add_node("sandbox_agent", sandbox_agent)
    .add_edge(START, "sandbox_agent")
    .add_edge("sandbox_agent", END)
)


if __name__ == "__main__":
    checkpointer = InMemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)

    output = graph.invoke(
        MessagesState(messages=[HumanMessage("What is the weather in sf?")]),
        config={"configurable": {"thread_id": "123"}},
    )

    print(output)


else:
    graph = graph_builder.compile()
