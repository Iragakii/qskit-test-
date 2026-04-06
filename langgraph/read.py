import os 
from typing import List , TypedDict , Union
from langchain_core.messages import HumanMessage , AIMessage
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph , START , END 

SUPPORT_EXT = (".jsx" , ".tsx" , ".js" , ".pdf" , ".md" , ".html" , ".css" , ".py")  
MAX_FILE_SIZE = 4000
MAX_TOTAL_SIZE = 12000


class AgentState(TypedDict) : 
    messages : List[Union[HumanMessage , AIMessage]]

llm = ChatOllama(model = "llama3")

def process(state : AgentState) -> AgentState : 
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

def read_file(path : str) -> str : 
    try : 
        with open(path , "r" , encoding ="utf-8") as f: 
            content = f.read()
        if len(content) > MAX_FILE_SIZE:
            content = content[:MAX_FILE_SIZE] + "\n... truncated"

        return content
    except Exception as e : 
        return f"[Error read : {path}] : {e}"
    

def get_all_files(folder : str) -> List[str] : 
    files = []

    for root , _ , filesname in os.walk(folder): 
        for name in filesname :
            if name.endswith(SUPPORT_EXT):
                files.append(os.path.join(root, name))
    return files
    
def load_multiple_files(paths : List[str]) -> str :
    combined = ""
    total_size = 0

    for path in paths : 
        if not os.path.exists(path):
            continue

        content = read_file(path)
        block = f"\n\n ###File : {path} \n {content}"
        total_size += len(block)

        if total_size > MAX_TOTAL_SIZE : 
            combined += "\n\n ...truncated"
            break
        combined += block
    return combined

def load_folder(folder : str) -> str:
    files = get_all_files(folder)
    print(f"Found Folder {len(files)} files")
    return load_multiple_files(files)

def handle_input(user_input : str) -> str :
    user_input = user_input.strip()

    if "," in user_input:
        paths = [p.strip() for p in user_input.split(",")]
        return load_multiple_files(paths)

    if os.path.isdir(user_input):
        return load_folder(user_input)
    if os.path.isfile(user_input) and user_input.endswith(SUPPORT_EXT):
        return load_multiple_files([user_input])
    
    return user_input

users_input = input("Enter :")


while users_input != "exit" : 
    processed_input = handle_input(users_input)

    if processed_input != users_input:
        messages_content = f"""
You are an AI codebase assistant.

Use the following REAL file content:

{processed_input}
"""
    else :
        messages_content = users_input
        conversation_history.append(HumanMessage(content = messages_content))
        result = agent.invoke({"messages" : conversation_history})

        conversation_history = result["messages"]

        users_input = input("Enter :")

    

with open("save.txt" , "w") as file :
    file.write("Chat His")
    for messages in conversation_history:
        if isinstance(messages , HumanMessage):
            file.write(f"You : {messages.content} \n")

        if isinstance(messages , AIMessage):
            file.write(f"AI : {messages.content} \n \n " )

    file.write("End")

print("Iragaki")