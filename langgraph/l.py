from typing import TypedDict , Annotated , Sequence 
from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage 
from langchain_core.messages import SystemMessage 
from langchain_community.chat_models import ChatOllama
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph , END
from langgraph.prebuilt import ToolNode



class AgentState(TypedDict) : 
    messages : Annotated[Sequence[BaseMessage] , add_messages]


@tool 
def add(a : int , b:int):
    """This is an addition func add 2 number together"""
    return a + b 
tools = [add]

model = ChatOllama(model = "llama3")

def model_call(state:AgentState) -> AgentState: 
    system_prompt = SystemMessage(content = """
                    You are an AI assistant
            If the user asks for math, use the tool 'add'.
            Return tool calls in correct format if needed.
""")

    response = model.invoke([system_prompt] + list(state["messages"]))
    return {"messages": [response]}   

def shuold_continue(state : AgentState): 
    messages = state["messages"]
    last_messages = messages[-1]
    if not hasattr(last_messages, "tool_calls") or not last_messages.tool_calls: 
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools" , tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent" ,
    shuold_continue,
    {
        "continue" : "tools", 
        "end" : END ,
    }
)
graph.add_edge("tools" , "our_agent")
app = graph.compile()

def print_stream(stream): 
    for s in stream: 
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
inputs = {"messages" : [("user" , "Add 3+4." )]}  
print_stream(app.stream(inputs, stream_mode="values")) 
     