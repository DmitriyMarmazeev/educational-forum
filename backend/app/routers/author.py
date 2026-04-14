from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas, auth
from app.models import User

router = APIRouter(prefix="/author", tags=["Author"])

@router.get("/stats", response_model=list[schemas.TaskStatsOut])
async def get_author_stats(
    current_user: User = Depends(auth.author_or_above),
    db: AsyncSession = Depends(get_db)
):
    tasks = await crud.get_tasks_by_author(db, current_user.id_user)
    stats = []
    for task in tasks:
        unique_views = await crud.get_unique_page_views(db, task.id_task)
        solution_views = await crud.get_unique_solution_views(db, task.id_task)
        ratings_count, avg_rating = await crud.get_rating_stats(db, task.id_task)
        stats.append(schemas.TaskStatsOut(
            id_task=task.id_task,
            unique_views=unique_views,
            solution_views=solution_views,
            ratings_count=ratings_count,
            average_rating=avg_rating
        ))
    return stats

@router.post("/payout", status_code=200)
async def request_payout(
    current_user: User = Depends(auth.author_or_above),
):
    # Заглушка
    return {"message": "Payout request received (stub)"}