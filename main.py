from fastapi import FastAPI

from app.routes.issues import router as issues_router

app = FastAPI()

app.include_router(issues_router)

# items = [
#     {"id": 1, "name": "Item One"},
#     {"id": 2, "name": "Item Two"},
#     {"id": 3, "name": "Item Three"},
# ]

items_counter = 4


@app.get("/health")
def health_check():
    return {"status": "ok"}


# @app.get("/items")
# def get_all_items():
#     return items


# @app.get("/items/{item_id}")
# def get_item_ById(item_id: int):
#     for item in items:
#         if item["id"] == item_id:
#             return item
#     return {"error": f"Item with id {item_id} not found"}


# @app.post("/items")
# def create_item(name: str):
#     global items_counter
#     new_item = {"id": items_counter, "name": f"{name}"}
#     items.append(new_item)
#     items_counter += 1
#     return new_item
