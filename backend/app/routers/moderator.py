from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_db
from app import crud, schemas, auth
from app.models import User, TaskStatus
from app.schemas import DeleteUserByEmailRequest

router = APIRouter(prefix="/moderator", tags=["Moderator"])

# Все эндпоинты требуют роли moderator или admin

@router.get("/tasks", response_model=List[schemas.TaskModeratorOut])
async def get_tasks_for_moderation(
    status: Optional[schemas.TaskStatusEnum] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(auth.moderator_or_above),
    db: AsyncSession = Depends(get_db)
):
    tasks = await crud.get_all_tasks_for_moderator(
        db, 
        status_filter=TaskStatus(status) if status else None,
        skip=skip, 
        limit=limit
    )
    result = []
    for task in tasks:
        author_name = f"{task.author.name} {task.author.surname}" if not task.author.is_deleted else "Удалённый аккаунт"
        result.append(schemas.TaskModeratorOut(
            id_task=task.id_task,
            condition=task.condition,
            image=task.image,
            answer=task.answer,
            task_number=task.task_number,
            status=task.status,
            author_name=author_name,
            subject_name=task.subject.subject_name,
            average_rating=await crud.get_average_rating(db, task.id_task),
            comments_count=await crud.get_comments_count(db, task.id_task),
            author_id=task.id_user,
            author_email=task.author.email if not task.author.is_deleted else None,
            created_at=task.created_at if hasattr(task, 'created_at') else None,
            updated_at=task.updated_at if hasattr(task, 'updated_at') else None
        ))
    return result

@router.patch("/tasks/{task_id}/status", response_model=schemas.TaskModeratorOut)
async def change_task_status(
    task_id: int,
    new_status: schemas.TaskStatusEnum,
    current_user: User = Depends(auth.moderator_or_above),
    db: AsyncSession = Depends(get_db)
):
    task = await crud.update_task_status(db, task_id, TaskStatus(new_status))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.refresh(task, attribute_names=['author', 'subject'])
    author_name = f"{task.author.name} {task.author.surname}" if not task.author.is_deleted else "Удалённый аккаунт"
    return schemas.TaskModeratorOut(
        id_task=task.id_task,
        condition=task.condition,
        image=task.image,
        answer=task.answer,
        task_number=task.task_number,
        status=task.status,
        author_name=author_name,
        subject_name=task.subject.subject_name,
        average_rating=await crud.get_average_rating(db, task.id_task),
        comments_count=await crud.get_comments_count(db, task.id_task),
        author_id=task.id_user,
        author_email=task.author.email if not task.author.is_deleted else None,
        created_at=task.created_at if hasattr(task, 'created_at') else None,
        updated_at=task.updated_at if hasattr(task, 'updated_at') else None
    )

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_moderator(
    task_id: int,
    current_user: User = Depends(auth.moderator_or_above),
    db: AsyncSession = Depends(get_db)
):
    success = await crud.delete_task_moderator(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return

@router.get("/comments", response_model=List[schemas.CommentModeratorOut])
async def get_comments_for_moderation(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(auth.moderator_or_above),
    db: AsyncSession = Depends(get_db)
):
    comments = await crud.get_all_comments_for_moderator(db, skip, limit)
    result = []
    for c in comments:
        user_name = f"{c.user.name} {c.user.surname}" if not c.user.is_deleted else "Удалённый аккаунт"
        task_preview = c.task.condition[:100] + "..." if len(c.task.condition) > 100 else c.task.condition
        result.append(schemas.CommentModeratorOut(
            id_task_comment=c.id_task_comment,
            comment=c.comment,
            task_id=c.id_task,
            user_id=c.id_user,
            user_email=c.user.email,
            created_at=getattr(c, 'created_at', None)
        ))
    return result

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_by_moderator(
    comment_id: int,
    current_user: User = Depends(auth.moderator_or_above),
    db: AsyncSession = Depends(get_db)
):
    success = await crud.delete_comment_moderator(db, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return

@router.delete("/users/by-email", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_email(
    request: DeleteUserByEmailRequest,
    current_user: User = Depends(auth.moderator_or_above),
    db: AsyncSession = Depends(get_db)
):
    success = await crud.soft_delete_user_by_email(db, request.email)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or cannot be deleted")
    return