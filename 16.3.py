from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, constr, conint
from typing import Dict

app = FastAPI()

# Начальный словарь пользователей
users: Dict[int, str] = {1: 'Имя: Example, возраст: 18'}

class UserInCreate(BaseModel):
    username: constr(min_length=1, max_length=50, strip_whitespace=True)  # username с минимальной длиной 1 и максимальной 50
    age: conint(ge=0, le=150)  # age должно быть целым числом от 0 до 150

class UserInUpdate(BaseModel):
    username: constr(min_length=1, max_length=50, strip_whitespace=True)
    age: conint(ge=0, le=150)

# GET запрос для получения всех пользователей
@app.get("/users")
async def get_users():
    return users

# POST запрос для добавления нового пользователя
@app.post("/user/")
async def create_user(user: UserInCreate):
    # Находим максимальный ключ в словаре
    user_id = max(users.keys(), default=0) + 1
    users[user_id] = f'Имя: {user.username}, возраст: {user.age}'
    return f"User {user_id} is registered"

# PUT запрос для обновления существующего пользователя
@app.put("/user/{user_id}/")
async def update_user(user_id: int, user: UserInUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = f'Имя: {user.username}, возраст: {user.age}'
    return f"User {user_id} has been updated"

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}/")
async def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return f"User {user_id} has been deleted"