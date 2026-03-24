from typing import Dict , TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    message : str 


def greeting_node(state : AgentState) -> AgentState: 
    """ Simple node greeting"""

    state['message'] = "Hey "+ state["message"] + ", how is ur day going" 
    return state 


graph = StateGraph(AgentState)

graph.add_node("greeter" , greeting_node)


graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

result = app.invoke({"message" : "Ira"})
print(result["message"])