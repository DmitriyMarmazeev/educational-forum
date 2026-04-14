from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas, auth
from app.models import User

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["Comments"])

@router.get("/", response_model=list[schemas.CommentOut])
async def get_comments(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(auth.get_current_user)
):
    comments = await crud.get_task_comments(db, task_id)
    return [
        schemas.CommentOut(
            id_task_comment=c.id_task_comment,
            comment=c.comment,
            status=c.status,
            user_name=f"{c.user.name} {c.user.surname}" if not c.user.is_deleted else "Удалённый аккаунт"
        )
        for c in comments
    ]

@router.post("/", response_model=schemas.CommentOut, status_code=status.HTTP_201_CREATED)
async def add_comment(
    task_id: int,
    comment_data: schemas.CommentCreate,
    current_user: User = Depends(auth.student_or_above),
    db: AsyncSession = Depends(get_db)
):
    # Проверить существование задачи
    task = await crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    comment = await crud.create_comment(db, task_id, current_user.id_user, comment_data.comment)
    return schemas.CommentOut(
        id_task_comment=comment.id_task_comment,
        comment=comment.comment,
        status=comment.status,
        user_name=f"{current_user.name} {current_user.surname}"
    )

# Удаление комментария возможно только автором комментария или админом (пока не реализовано)