import asyncio
import json
import sys

from sqlalchemy import select
from app.database import AsyncSessionLocal, engine
from app.models import Base, User


async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_db():
    # Наполнение тестовыми данными
    async with AsyncSessionLocal() as session:
        db = AsyncSessionLocal()
        user = User(email="test@example.com", name="Test User")
        db.add(user)
        await db.commit()
        db.close()


async def get_user_by_email(email: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        if user:
            print(json.dumps({"id_user": user.id_user, "email": user.email}))
        else:
            print(json.dumps(None))

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "reset":
        asyncio.run(reset_db())
    elif command == "seed":
        asyncio.run(seed_db())
    elif command == "getUserByEmail":
        asyncio.run(get_user_by_email(sys.argv[2]))
