from typing import TypedDict 
from langgraph.graph import StateGraph 

class AgentState(TypedDict) : 
    name : str
    age : str 
    final : str 


def first_node(state : AgentState) -> AgentState : 

    state["final"] = f"{state.get('name')}"
    return state 

def second_node(state : AgentState) -> AgentState : 
    state["final"] = state["final"] + f"U are {state.get('age')}  years old . "
    return state 

graph = StateGraph(AgentState)
graph.add_node("first_node"  , first_node )
graph.add_node("second_node" , second_node)
graph.set_entry_point("first_node")
graph.add_edge("first_node" , "second_node")
graph.set_finish_point("second_node")
app = graph.compile()

print_first = app.invoke({"name" : "Iragaki"  , "age" :"1999" })


print(print_first)
