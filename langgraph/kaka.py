import os
import requests
from typing import TypedDict, List, Union

from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatOllama

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

GOOGLE_API_KEY = "AIzaSyDBBdqCdJz_p1b6CmDt1VTPV73nJe4JgIs"
YOUTUBE_API_KEY = "AIzaSyDDxbvIbqIH6IK0zpuNfN9Ld1DQndBsAEk"
GOOGLE_CX = "25068496642b544ae"

llm = ChatOllama(model = "llama3")

def google_search(query : str) : 
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q" : query , 
        "key" : GOOGLE_API_KEY , 
        "cx" :   GOOGLE_CX
    } 
    res = requests.get(url ,params = params)
    return res.json()

def youtube_search(query : str) : 
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part" : "snippet", 
        "q" : query,
        "key" : YOUTUBE_API_KEY , 
        "maxResults" : 5,
        "type" : "video"

    }
    res = requests.get(url , params = params)
    return res.json()

class AgentState(TypedDict) : 
    messages : List[Union[HumanMessage , AIMessage]]


def process(state: AgentState) -> AgentState:
    user_input = state["messages"][-1].content

    # Detect intent simple way
    if "youtube" in user_input.lower():

        result = youtube_search(user_input)

        items = result.get("items", [])
        if not items:
            response_text = "No results found."

        else:
            top = items[0]
            video_id = top["id"]["videoId"]
            title = top["snippet"]["title"]

            link = f"https://www.youtube.com/watch?v={video_id}"

            response_text = f"🎵 {title}\n🔗 {link}"

    elif "google" in user_input.lower() or "search" in user_input.lower():

        result = google_search(user_input)

        items = result.get("items", [])
        if not items:
            response_text = "No results found."
        else:
            top = items[0]
            title = top["title"]
            link = top["link"]

            response_text = f"🔎 {title}\n🔗 {link}"

    else:
        response = llm.invoke(state["messages"])
        response_text = response.content

    state["messages"].append(AIMessage(content=response_text))
    print("AI:", response_text)

    return state

graph = StateGraph(AgentState)
graph.add_node("process_node" , process)
graph.add_edge(START , "process_node")
graph.add_edge("process_node", END)

agent = graph.compile()

conversation_history = []

while True : 
    users_input = input("Enter :")

    if users_input.lower() == "exit":
        break

    conversation_history.append(HumanMessage(content=users_input))
    result = agent.invoke({"messages" : conversation_history})
    conversation_history = result["messages"]

