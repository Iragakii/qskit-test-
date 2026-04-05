import os 
from typing import List , TypedDict , Union
from langchain_core.messages import HumanMessage , AIMessage
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph , START , END 

class AgentState(TypedDict) :
    messages : List[Union[HumanMessage , AIMessage]]

llm = ChatOllama(model = "llama3")

def process(state : AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content = response.content))
    print(f"\n AI : {response.content}")

    return state

graph = StateGraph(AgentState)
graph.add_node("process_node" , process)
graph.add_edge(START , "process_node")
graph.add_edge("process_node" , END)

agent = graph.compile()

conversation_history = []
users_input = input("Enter :")

while users_input != "exit":
    conversation_history.append(HumanMessage(content = users_input))
    result = agent.invoke({"messages" : conversation_history})
    conversation_history = result["messages"]

    users_input = input("Enter :")

with open("longging.txt" , "w") as file:
    file.write("Chat Hisotry")
    for messages in conversation_history:
        if isinstance(messages , HumanMessage):
            file.write(f"You: {messages.content}")
        if isinstance(messages , AIMessage):
            file.write(f"AI : {messages.content}")
    file.write("End Chat")
print("done")