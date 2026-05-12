import os
import requests
from typing import TypedDict, List, Union
import webbrowser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatOllama

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
import requests
GOOGLE_API_KEY = "AIzaSyDBBdqCdJz_p1b6CmDt1VTPV73nJe4JgIs"
YOUTUBE_API_KEY = "AIzaSyDDxbvIbqIH6IK0zpuNfN9Ld1DQndBsAEk"
GOOGLE_CX = "25068496642b544ae"

# =========================
# LLM
# =========================
llm = ChatOllama(model="llama3")


# =========================
# LYRICS API
# =========================
def get_lyrics(artist, title):
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json().get("lyrics", "Lyrics not found.")
        else:
            return "Lyrics not found."

    except Exception:
        return "Lyrics API error."


# =========================
# SEARCH FUNCTIONS
# =========================
def google_search(query: str):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX
    }
    return requests.get(url, params=params).json()


def youtube_search(query: str):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": 1,
        "type": "video"
    }
    return requests.get(url, params=params).json()


# =========================
# STATE
# =========================
class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]


# =========================
# PROCESS NODE
# =========================
def process(state: AgentState) -> AgentState:
    user_input = state["messages"][-1].content
    response_text = ""

    # -------- YOUTUBE --------
    if "play" in user_input.lower():

        result = youtube_search(user_input)
        items = result.get("items", [])

        if items:
            top = items[0]

            video_id = top["id"]["videoId"]
            title = top["snippet"]["title"]

            # Open browser
            webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")

            # Try simple artist/title split
            if "-" in title:
                artist, song = title.split("-", 1)
                artist = artist.strip()
                song = song.strip()
            else:
                artist = ""
                song = title

            lyrics = get_lyrics(artist, song)

            response_text = f"""
🎵 Playing: {title}

📝 Lyrics:

{lyrics}
"""

        else:
            response_text = "No YouTube results found."

    # -------- GOOGLE --------
    elif "google" in user_input.lower() or "search" in user_input.lower():

        result = google_search(user_input)
        items = result.get("items", [])

        if items:
            top = items[0]
            response_text = f"🔎 {top['title']}\n🔗 {top['link']}"
        else:
            response_text = "No results found."

    # -------- NORMAL CHAT --------
    else:
        response = llm.invoke(state["messages"])
        response_text = response.content

    state["messages"].append(AIMessage(content=response_text))
    print("AI:", response_text)

    return state


# =========================
# BUILD GRAPH
# =========================
graph = StateGraph(AgentState)
graph.add_node("process_node", process)
graph.add_edge(START, "process_node")
graph.add_edge("process_node", END)

agent = graph.compile()


# =========================
# CHAT LOOP
# =========================
conversation_history = []

while True:
    users_input = input("Enter: ")

    if users_input.lower() == "exit":
        break

    conversation_history.append(HumanMessage(content=users_input))

    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]