from langgraph.graph import StateGraph , END
import random 
from typing import Dict , List , TypedDict

class AgentState(TypedDict) : 
    name : str
    number : List[int]
    counter : int 

def greeting(state : AgentState) -> AgentState : 
    state["name"] = f"Hello {state.get('name')}"
    state["counter"] = 0
    return state

def random_1(state : AgentState) -> AgentState : 
    state["number"].append(random.randint(0 ,10))
    state["counter"] += 1
    return state

def decide(state: AgentState) -> AgentState : 
    if state["counter"] < 5 : 
        print("Enteringg Loop" ,state["number"])
        return "loop"
    else :
        return "exit"
    
graph = StateGraph(AgentState)
graph.add_node("greeting_node" , greeting)
graph.add_node("random_node" , random_1)
graph.add_edge("greeting_node" , "random_node")
graph.add_conditional_edges(
    "random_node",
    decide,
    {
        "loop" : "random_node",
        "exit" : END 

    }
) 
graph.set_entry_point("greeting_node")
app = graph.compile()

result = app.invoke({"name" : "iragaki" , "number" : [] , "counter" : -100})
print(result)