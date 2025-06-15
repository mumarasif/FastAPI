from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(tile="To-do API")

db = []

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do API!"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return db

@app.post("/tasks", response_model= Task)
def create_task(task: Task):
    for existing_task in db:
        if existing_task["id"] == task.id:
            raise HTTPException(status_code=400, detail="Task with this id already exists")
    db.append(task.model_dump())
    return task

@app.put("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    for task in db:
        if int(task["id"]) == int(task_id):
            task["completed"] = True
            return task
    raise HTTPException(status_code=404, detail= "Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id = int):
    for task in db:
        if int(task["id"]) == int(task_id):
            db.remove(task)
            return{"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
            