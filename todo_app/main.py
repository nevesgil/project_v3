from fastapi import FastAPI
from database.database import engine, SessionLocal
from database import models
from todo_app.routers import auth, todos, admin, users

app = FastAPI()

# it creates my database tables
models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
