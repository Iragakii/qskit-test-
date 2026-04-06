import os 
from typing import List , TypedDict , Union
from langchain_core.messages import HumanMessage , AIMessage
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph , START , END 


SUPPORT_EXT = (".jsx" , ".js" , ".tsx" , ".html" , ".css" , ".pdf" , ".md")
MAX_FILE_SIZE = 4000
MAX_TOLTAL_SIZE = 12000

class AgentState(TypedDict):
    messages : List[Union[HumanMessage , AIMessage]]

llm = ChatOllama("llama3")

def process(state:AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content = response.content))

    print(f"\n AI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process_node" , process)
graph.add_edge(START , "process_node")
graph.add_edge("process_node" , END)

agent = graph.compile()

conversation_history = []

def read_file(path : str) -> str:
    try : 
        with open(path , "r" , encoding ="utf-8") as f:
            content = f.read()
        if len(content) > MAX_FILE_SIZE:
            content = content(:MAX_FILE_SIZE) + "\n...truncated"
        return content
    except Exception as e:
        return f"[Error Read : {path}] : {e}"

def get_all_files(folder : str) -> str:
    files = []
    for root , _ , filesname in os.walk(folder):
        for name in filesname:
            if name.endswith(SUPPORT_EXT):
                files.append(os.path.join(root, name))
    return files

