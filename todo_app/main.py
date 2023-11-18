from fastapi import FastAPI, Depends, HTTPException, Path, Query
from database.database import engine, SessionLocal
from database import models
from database.models import Todos, Second
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from todo_app.request import TodoRequest
from routers import auth_v2

app = FastAPI()

# it creates my database tables
models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Route to get all todos
@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@app.get("/secret")
async def read_secret(db: db_dependency):
    return db.query(Todos).join(Second, Second.id == Todos.id).all()


@app.get("/todo/", status_code=status.HTTP_200_OK)
async def read_complete_todo(db: db_dependency, complete: int):
    todo_model = db.query(Todos).filter(Todos.complete == bool(complete)).all()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not fount")


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not found")
    # db.query(Todos).filter(Todos.id == todo_id).delete()
    db.delete(todo_model)
    db.commit()
