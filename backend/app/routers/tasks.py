from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app import crud, schemas, auth
from app.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[schemas.TaskOut])
async def list_tasks(
    subject_id: Optional[int] = Query(None),
    task_number: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Возвращает список задач. Доступно всем, включая гостей.
    """
    tasks = await crud.get_tasks_with_filter(db, subject_id, task_number, skip, limit)
    result = []
    for task in tasks:
        author_name = f"{task.author.name} {task.author.surname}" if not task.author.is_deleted else "Удалённый аккаунт"
        avg_rating = await crud.get_average_rating(db, task.id_task)
        comments_count = await crud.get_comments_count(db, task.id_task)
        result.append(schemas.TaskOut(
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
        ))
    return result

@router.get("/{task_id}", response_model=schemas.TaskOut)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Публичный просмотр задачи. Возвращает условие, ответ, автора и т.д., но НЕ решение.
    Если пользователь авторизован — фиксируется просмотр страницы.
    """
    task = await crud.get_task_detail(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Логируем просмотр страницы (только для авторизованных)

    author_name = f"{task.author.name} {task.author.surname}" if not task.author.is_deleted else "Удалённый аккаунт"
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

@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: schemas.TaskCreate,
    current_user: User = Depends(auth.author_or_above),
    db: AsyncSession = Depends(get_db)
):
    task = await crud.create_task(db, task_data, current_user.id_user)
    # возвращаем созданную задачу
    return await get_task(task.id_task, db)

@router.put("/{task_id}", response_model=schemas.TaskOut)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    current_user: User = Depends(auth.author_or_above),
    db: AsyncSession = Depends(get_db)
):
    task = await crud.update_task(db, task_id, task_update, current_user.id_user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not owned by you")
    return await get_task(task.id_task, db)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(auth.author_or_above),
    db: AsyncSession = Depends(get_db)
):
    success = await crud.delete_task_by_author(db, task_id, current_user.id_user)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found or not owned by you")
    return


@router.get("/{task_id}/solution", response_model=schemas.TaskSolutionOut)
async def get_task_solution(
    task_id: int,
    current_user: User = Depends(auth.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получение решения задачи.
    Доступно только авторизованным пользователям с активной подпиской,
    либо автору задачи.
    """
    task = await crud.get_task_detail(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Проверяем доступ к решению
    has_subscription = (
        current_user.subscribed_until_date and
        current_user.subscribed_until_date > datetime.now(timezone.utc)
    )
    is_author = current_user.id_user == task.id_user
    # Привилегированные роли тоже могут видеть (авторы и админы)
    is_privileged = current_user.role.role_name in ["admin"]

    if not (has_subscription or is_author or is_privileged):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Active subscription required to view solution"
        )

    # Логируем просмотр решения (уникальный)
    await crud.add_solution_view(db, current_user.id_user, task_id)

    return schemas.TaskSolutionOut(solution=task.solution)

@router.post("/{task_id}/rate", response_model=schemas.RatingOut)
async def rate_task(
    task_id: int,
    rating_data: schemas.RatingCreate,
    current_user: User = Depends(auth.student_or_above),
    db: AsyncSession = Depends(get_db)
):
    task = await crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Проверяем, не оценивал ли уже
    existing = await crud.get_user_rating(db, task_id, current_user.id_user)
    if existing:
        # Обновляем оценку
        rating = await crud.update_rating(db, existing.id_task_rating, rating_data.rating)
    else:
        rating = await crud.create_rating(db, task_id, current_user.id_user, rating_data.rating)
    return schemas.RatingOut(
        id_task_rating=rating.id_task_rating,
        rating=rating.rating,
        id_task=rating.id_task,
        user_name=f"{current_user.name} {current_user.surname}"
    )