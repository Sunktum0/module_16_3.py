from fastapi import FastAPI, HTTPException
from typing import Dict

app = FastAPI()

# Начальный словарь пользователей
users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}

# GET запрос для получения всех пользователей
@app.get("/users")
async def get_users():
    return users

# POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}")
async def create_user(username: str, age: int):
    # Находим максимальный ключ в словаре
    user_id = str(max(int(uid) for uid in users.keys()) + 1)
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"User {user_id} is registered"

# PUT запрос для обновления существующего пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: str, username: str, age: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"User {user_id} has been updated"

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}")
async def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return f"User {user_id} has been deleted"