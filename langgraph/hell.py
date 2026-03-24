from typing import TypedDict , List 
from langgraph.graph import StateGraph

class AgentState(TypedDict) :
    values : List[int]
    name : str 
    result : str 


def process_values(state : AgentState) -> AgentState:
    """This is fuynct handle multiple different input"""
    state["result"] = f"Hi thre {state['name']}! Your sum = {sum(state['values'])}"
    return state
graph  = StateGraph(AgentState)
graph.add_node("processor" , process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")
app = graph.compile()

ans = app.invoke({"values" : [1 , 2 ,3 ,4 ] , "name" : "Ira"})
print(ans["result"])