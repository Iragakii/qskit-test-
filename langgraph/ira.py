from typing import TypedDict 
from langgraph.graph import StateGraph , START ,END 

class AgentState(TypedDict) : 
    number1 : int 
    operation : str
    number2 : int
    number3 : int 
    operation2 : str 
    number4 : int 
    FinalNum : int
    FinalNum2 : int  


def subtractor1(state : AgentState) -> AgentState : 
    state["FinalNum"] = (state.get('number1')  - state.get('number2'))                                                          
    return state 
def subtractor2(state :AgentState) -> AgentState : 
    state["FinalNum"] = state.get("FinalNum") - (state.get('number3') - state.get('number4'))   
    return state
def adder(state: AgentState) -> AgentState : 
    state["FinalNum2"] = (state.get('number1') - state.get('number2') - state.get('number3')) 
    return state
def adder2(state : AgentState ) -> AgentState : 
    state["FinalNum2"] = state.get("FinalNum2") + state.get("number4")
    return state
def decide_next_node(state : AgentState) -> AgentState : 
    if state["operation"] == "-" : 
        return "subtractor2_operation"
    if state["operation2"] == "+"  : 
        return "adder_operation"
    return "end"
   

graph = StateGraph(AgentState)
graph.add_node("subtractor1_node" , subtractor1)
graph.add_node("subtractor2_node" , subtractor2)
graph.add_node("adder_node" , adder)
graph.add_node("adder2_node" , adder2)

graph.add_edge(START  , "subtractor1_node")
graph.add_conditional_edges(
    "subtractor1_node" , 
    decide_next_node,
    {
        "subtractor2_operation" : "subtractor2_node",
        "adder_Operation" : "adder_node",
        "end" : END 
        

    }
)


 
graph.add_edge("subtractor2_node" , END)

graph.add_edge("adder2_node" , END)

app = graph.compile()

initial_state = AgentState(number1 = 10 , operation="-" , number2= 5 , number3 = 7 , number4 = 2 , operation2="+" , FinalNum= 0 , FinalNum2 = 0)
print(app.invoke(initial_state))

