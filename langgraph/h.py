from typing import TypedDict
from langgraph.graph import StateGraph , START , END

class AgentState(TypedDict) : 
    number1 : int
    operator : str
    number2 : int
    FinalNum : int 

def adder(state: AgentState) -> AgentState : 
    state["FinalNum"] = state.get('number1') + state.get('number2')
    return state
def subtrator(state : AgentState) -> AgentState : 
    state["FinalNum"] = state.get('number1') - state.get('number2')
    return state

def decide_next_node(state : AgentState) -> AgentState : 
    if state["operator"] == "+" :
        return "addition_operation" 
    elif state["operator"] == "-" :
        return "subtractor_operation"
    
graph  = StateGraph(AgentState)

graph.add_node("add_node" , adder )
graph.add_node("subbtrac_node" , subtrator)
graph.add_node("router" , lambda state:state)
graph.add_edge(START , "router")
graph.add_conditional_edges(
    "router" , 
    decide_next_node,
    {
        "addition_operation" : "add_node" , 
        "subractor_operation" : "subbtrac_node"
    }
)
graph.add_edge("add_node" , END)
graph.add_edge("subbtrac_node" , END)
app = graph.compile()

initial_state_1 = AgentState(number1 = 10 , operator="+" , number2 = 5)
print(app.invoke(initial_state_1))