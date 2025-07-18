from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


def get_small_model():
    # return ChatOpenAI(model="gpt-4o-mini")
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")
    return ChatOpenAI(model="gpt-4.1-nano")


def get_large_model():
    # 4.1-nano was not smart enough, even for testing
    # return ChatOpenAI(model="gpt-4o")
    # return ChatGoogleGenerativeAI(model="gemini-2.0-flash") # Doesn't work

    # return ChatOpenAI(model="qwen3-14b-mlx", base_url="http://localhost:1234/v1")
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    # return ChatOpenAI(model="gpt-4.1-mini")
    # return ChatOpenAI(model="o4-mini")
    # return ChatOpenAI(model="gpt-4.1")
    # return ChatOpenAI(model="gpt-4o")
    # return ChatOpenAI(model="gpt-4o")
    return ChatOpenAI(model="gpt-4o-mini")
