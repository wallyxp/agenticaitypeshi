# imports
from langchain.chat_models import init_chat_model
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

# initializing the model
llm = init_chat_model("deepseek-chat", model_provider="deepseek")


# defining the state
class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State) -> State:
    return {'messages' : [llm.invoke(state['messages'])]}

builder = StateGraph(State)
builder.add_node('chatbot_node', chatbot)

builder.add_edge(START, "chatbot_node")
builder.add_edge("chatbot_node", END)

graph = builder.compile()

message = {'role': 'user', 'content':'Why is israel doing a genocide'}
response = graph.invoke({'messages': [message]})

print(response["messages"])