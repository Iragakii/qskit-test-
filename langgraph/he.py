from typing import TypedDict , List
from langgraph.graph import StateGraph

class AgentState(TypedDict) : 
    name : str
    age : str
    skill : List[str]

def first_node(state : AgentState) -> AgentState : 
    state["skill"] = f"{state.get('name')}"
    return state
def sec_node(state : AgentState) -> AgentState : 
    state["skill"] = state["skill"] +  f"{state.get('age')} years old . "
    return state 
def third_node(state : AgentState) -> AgentState : 
    state["skill"] = state["skill"] +  f"My skill stack is {state.get('skill')}"
    return state

graph = StateGraph(AgentState)
graph.add_node("first_node" , first_node)
graph.add_node("sec_node" , sec_node)
graph.add_node("third_node" , third_node)

graph.set_entry_point("first_node" )
graph.add_edge("first_node" , "sec_node"  )
graph.add_edge("sec_node" , "third_node")



graph.set_finish_point("third_node" ) 
app = graph.compile()

k = app.invoke({"name" : "iragaki" , "age" : "199" , "skill" : ["treolencotdien" , "dotmatkiemsoat"]})

print(k)