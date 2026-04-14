from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, users, subjects, tasks, comments, ratings, author, moderator, admin

app = FastAPI(title="Educational Forum API")

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
# app.include_router(subjects.router)
app.include_router(tasks.router)
app.include_router(comments.router)
# app.include_router(ratings.router)
app.include_router(author.router)
app.include_router(moderator.router)
app.include_router(admin.router)


# @app.on_event("startup")
# async def init_db():
#     # В реальном проекте используйте Alembic для миграций
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to Educational Forum API"}