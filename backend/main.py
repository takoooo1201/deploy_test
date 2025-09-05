from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime

app = FastAPI(title="Test API", description="Simple API for deployment testing")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
DB_USERNAME = os.getenv("DB_USERNAME", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password123")

# MongoDB connection string
MONGODB_URL = f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@mongodb:27017/"

client = AsyncIOMotorClient(MONGODB_URL)
database = client.testdb
collection = database.tasks

# Pydantic models
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime

@app.on_event("startup")
async def startup_event():
    """Test database connection on startup"""
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

@app.get("/")
async def root():
    return {"message": "Backend API is running!", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks():
    """Get all tasks"""
    tasks = []
    async for task in collection.find():
        tasks.append(TaskResponse(
            id=str(task["_id"]),
            title=task["title"],
            description=task.get("description"),
            completed=task["completed"],
            created_at=task["created_at"]
        ))
    return tasks

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: Task):
    """Create a new task"""
    task_dict = task.dict()
    task_dict["created_at"] = datetime.now()
    
    result = await collection.insert_one(task_dict)
    
    created_task = await collection.find_one({"_id": result.inserted_id})
    
    return TaskResponse(
        id=str(created_task["_id"]),
        title=created_task["title"],
        description=created_task.get("description"),
        completed=created_task["completed"],
        created_at=created_task["created_at"]
    )

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    """Update a task"""
    from bson import ObjectId
    
    try:
        object_id = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    result = await collection.update_one(
        {"_id": object_id},
        {"$set": task.dict()}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task updated successfully"}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    from bson import ObjectId
    
    try:
        object_id = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    result = await collection.delete_one({"_id": object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
