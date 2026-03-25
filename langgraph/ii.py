from langgraph.graph import StateGraph , END
import random
from typing import List , Dict , TypedDict 

class AgentState(TypedDict) :
    player_name : str 
    guesses : List[int]
    attemps : int
    lower_bound : int
    upper_bound : int 
    bound : int


def setup_node(state :AgentState ) -> AgentState : 
    state["player_name"] = f"Hello {state.get('player_name')}"
    state["bound"] = random.randint(1 , 20)

    state["attemps"] = 0
    return state

def guess_node(state : AgentState) -> AgentState  : 
   
    
    state["guesses"] = int(input("Input Guess Number :"))
    print(state["guesses"])
    state["attemps"] += 1 
    return state 

def input_node(state: AgentState) -> str:
    if state["guesses"] == state["bound"]:
        print("🎉 Correct!")
        return "exit"

    if state["attemps"] >= 7:
        print(f"❌ Out of attempts. Number was {state['bound']}")
        return "exit"

    if state["guesses"] < state["bound"]:
        print("⬆️ Higher!")

    else:
        print("⬇️ Lower!")

    return "loop"

     
graph = StateGraph(AgentState)
graph.add_node("setup_node" , setup_node)
graph.add_node("guess_node" , guess_node)
graph.add_edge("setup_node" , "guess_node")

graph.add_conditional_edges(
    "guess_node",
    input_node, 
    {
        "loop" : "guess_node",
        "exit": END     
        }


)
graph.set_entry_point("setup_node")
app = graph.compile()

result = app.invoke({"player_name" : "Iragaki" , "guesses" : [] , "attemps" : 0 , "lower_bound" : 1 , "upper_bound" :20} )
print(result)

