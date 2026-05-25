from fastapi import APIRouter, Depends, HTTPException,Query
from typing import List, Optional
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
    db: AsyncSession = Depends(get_db)
):
    try:
        balance = current_user.wallet if current_user.wallet else 0.0
    except (ValueError, TypeError):
        balance = 0.0

    if balance <= 0:
        raise HTTPException(status_code=400, detail="No funds to withdraw")

    # Обнуляем кошелёк
    current_user.wallet = 0
    await db.commit()

    return {"message": f"{balance:.2f} рублей перечислено вам на карту", "paid_amount": balance}
@router.get("/tasks", response_model=List[schemas.TaskOut])
async def get_my_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: User = Depends(auth.author_or_above),
    db: AsyncSession = Depends(get_db)
):
    """
    Возвращает все задачи текущего автора (любой статус: draft, public, rejected, archived).
    """
    tasks = await crud.get_all_tasks_by_author(db, current_user.id_user, skip=skip, limit=limit)
    
    # Дополнительно подгружаем статистику для каждой задачи (рейтинг, кол-во комментариев)
    result = []
    for task in tasks:
        # Для черновиков/отклонённых можно не показывать рейтинг, но оставим как есть
        avg_rating = await crud.get_average_rating(db, task.id_task)
        comments_count = await crud.get_comments_count(db, task.id_task)
        # Имя автора – текущий пользователь (не удалён), поэтому можно взять из current_user
        # Но если author удалён – в задаче всё равно лежит id_user, но current_user != author? 
        # Для своих задач автор всегда видит своё имя.
        author_name = f"{current_user.name} {current_user.surname}"
        result.append(schemas.TaskOut(
            id_task=task.id_task,
            condition=task.condition,
            image=task.image,
            answer=task.answer,
            task_number=task.task_number,
            status=task.status,
            author_name=author_name,
            subject_name=task.subject.subject_name if task.subject else "",
            average_rating=avg_rating,
            comments_count=comments_count
        ))
    return result

@router.get("/{task_id}", response_model=schemas.TaskOut)
async def get_task(
    task_id: int,
    current_user: User = Depends(auth.author_or_above),
    db: AsyncSession = Depends(get_db),
):
    """
    Публичный просмотр задачи. Возвращает условие, ответ, автора и т.д., но НЕ решение.
    Если пользователь авторизован — фиксируется просмотр страницы.
    """
    task = await crud.get_author_task_detail(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Логируем просмотр страницы (только для авторизованных)

    author_name = f"{current_user.name} {current_user.surname}"
    avg_rating = await crud.get_average_rating(db, task.id_task)
    comments_count = await crud.get_comments_count(db, task.id_task)

    return schemas.TaskOut(
        id_task=task.id_task,
        condition=task.condition,
        image=task.image,
        answer=task.answer,
        task_number=task.task_number,
        status=task.status,
        author_name=author_name,
        subject_name=task.subject.subject_name,
        average_rating=avg_rating,
        comments_count=comments_count
    )
