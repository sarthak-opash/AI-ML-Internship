from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items/")
def create_item(item: dict):
    """
    Create an item.

    Args:
        item: dict
            Item to be created

    Returns:
        dict
            Item created
    """
    return {"item": item}


