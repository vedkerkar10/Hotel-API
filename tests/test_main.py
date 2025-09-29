# # test_main.py
# from fastapi.testclient import TestClient
# from routers.rooms_crud import router  # Assuming you have a rooms_crud.py with an 'app' instance

# client = TestClient(router)

# def test_read_root():
#     # r = client.get("/")
#     # assert r.status_code == 200
#     pass

# def test_create_and_get_room():
#     payload = {"number": "200", "type": "double", "price": 120, "capacity": 2}
#     r = client.post("/rooms/", json=payload)
#     assert r.status_code == 200
#     data = r.json()
#     assert data["number"] == "200"
#     rid = data["id"]
#     r2 = client.get(f"/rooms/{rid}")
#     assert r2.status_code == 200

from fastapi import FastAPI
from fastapi.testclient import TestClient
# from routers.auth import get_current_user
 
# from routers.rooms_crud import router
 
app = FastAPI()
# app.include_router(router)
client = TestClient(app)
 
def test_read_root():
    # r = client.get("/")
    # assert r.status_code == 200
    pass
 
# def test_create_and_get_room():
#     payload = {"number":"200","type":"double","price":120,"capacity":2}
#     r = client.post("/rooms/", json=payload)
#     assert r.status_code == 200
#     data = r.json()
#     assert data["number"] == "200"
#     rid = data["id"]
#     r2 = client.get(f"/rooms/{rid}")
#     assert r2.status_code == 200