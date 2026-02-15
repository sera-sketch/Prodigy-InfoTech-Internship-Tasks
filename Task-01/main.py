from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# User Model
class User(BaseModel):
    id: int
    name: str
    email: str

# Temporary database (in-memory)
users: List[User] = []

# Create User
@app.post("/users")
def create_user(user: User):
    for existing_user in users:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="User ID already exists")
    users.append(user)
    return {"message": "User created successfully", "user": user}

# Get All Users
@app.get("/users")
def get_users():
    return users

# Get User by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Update User
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            return {"message": "User updated successfully", "user": updated_user}
    raise HTTPException(status_code=404, detail="User not found")

# Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return {"message": "User deleted successfully", "user": deleted_user}
    raise HTTPException(status_code=404, detail="User not found")

