from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}

@app.post("/items/")
async def create_item(item: dict):
    return {"item": item}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "updated_item": item}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"Item with id {item_id} has been deleted."}

@app.get("/health")
async def health_check():
    return {"status": "OK"}