from fastapi import FastAPI, Query


app = FastAPI()



items = []

@app.get("/")

def root() : 
    return {"Hello" : "World"}


@app.post("/items")
def list_items(item: str = Query(...)) :
    items.append(item)
    return items\
    
@app.get("/items/{item_id}")
def get_item(item_id: int):   
    if item_id < len(items):       
        return items[item_id]  
    return {"error": "Item not found"}
@app.get("/items")
def get_items():  
    return items
