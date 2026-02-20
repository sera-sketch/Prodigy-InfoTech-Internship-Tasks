from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, User  # your models.py
from database import engine, SessionLocal  # your db connection file
from redis_client import r  # Redis client
import json

# Create DB tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API with Redis Cache")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------
# GET all users with caching
# ---------------------
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    # Try to get cached data first
    cached_users = r.get("all_users")
    if cached_users:
        return json.loads(cached_users)  # Return cached JSON

    # If cache miss, fetch from DB
    users = db.query(User).all()
    result = [
        {"id": u.id, "name": u.name, "email": u.email, "role": u.role}
        for u in users
    ]

    # Cache the result for 60 seconds
    r.set("all_users", json.dumps(result), ex=60)

    return result

# ---------------------
# Create a new user
# ---------------------
@app.post("/create_user")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Invalidate cache after adding new user
    r.delete("all_users")

    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

# ---------------------
# Delete a user
# ---------------------
@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

    # Invalidate cache after deletion
    r.delete("all_users")

    return {"detail": f"User {user_id} deleted successfully"}