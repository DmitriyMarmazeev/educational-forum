from sqlalchemy import select, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from datetime import datetime, timezone
from typing import Optional, List
from app.models import (
    TaskStatus, User, Role, Subject, Task, ViewHistory, SolutionView, 
    TaskRating, TaskComment
)
from app.schemas import UserCreate, UserUpdate, TaskCreate, TaskUpdate
from app.auth import get_password_hash, verify_password

# ---------- Users ----------
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id_user == user_id))
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(db, email)
    if not user or user.is_deleted:
        return None
    if not verify_password(password, user.password):
        return None
    return user

async def create_user(db: AsyncSession, user_data: UserCreate, role_name: str = "student") -> Optional[User]:
    existing = await get_user_by_email(db, user_data.email)
    if existing:
        return None
    role_res = await db.execute(select(Role).where(Role.role_name == role_name))
    role = role_res.scalar_one()
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        surname=user_data.surname,
        password=hashed_password,
        id_role=role.id_role,
        is_deleted=False
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user: User, user_update: UserUpdate) -> User:
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    for field, value in update_data.items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user

async def soft_delete_user(db: AsyncSession, user: User):
    user.is_deleted = True
    user.name = "Удалённый"
    user.surname = "аккаунт"
    user.email = f"deleted_{user.id_user}@deleted.com"
    user.password = ""
    user.wallet = None
    user.subscribed_until_date = None
    await db.commit()

# ---------- Subjects ----------
async def get_subjects(db: AsyncSession) -> List[Subject]:
    result = await db.execute(select(Subject).order_by(Subject.subject_name))
    return result.scalars().all()

async def create_subject(db: AsyncSession, subject_name: str) -> Subject:
    subject = Subject(subject_name=subject_name)
    db.add(subject)
    await db.commit()
    await db.refresh(subject)
    return subject

# ---------- Tasks ----------
async def get_tasks_with_filter(
    db: AsyncSession,
    subject_id: Optional[int] = None,
    task_number: Optional[int] = None,
    skip: int = 0,
    limit: int = 20
) -> List[Task]:
    query = (
        select(Task)
        .options(joinedload(Task.subject), joinedload(Task.author))
        .where(Task.status == TaskStatus.public)
    )
    if subject_id:
        query = query.where(Task.id_subject == subject_id)
    if task_number:
        query = query.where(Task.task_number == task_number)
    query = query.offset(skip).limit(limit).order_by(Task.id_task)
    result = await db.execute(query)
    return result.unique().scalars().all()

async def get_task_detail(db: AsyncSession, task_id: int) -> Optional[Task]:
    query = (
        select(Task)
        .options(joinedload(Task.subject), joinedload(Task.author))
        .where(Task.id_task == task_id, Task.status == TaskStatus.public)
    )
    result = await db.execute(query)
    return result.unique().scalar_one_or_none()

async def get_task_by_id(db: AsyncSession, task_id: int) -> Optional[Task]:
    result = await db.execute(select(Task).where(Task.id_task == task_id))
    return result.scalar_one_or_none()

async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    task = Task(**task_data.dict(), id_user=user_id, status="active")
    db.add(task)
    await db.commit()
    await db.refresh(task)
    # Обновить счётчик задач в предмете
    subject = await db.get(Subject, task.id_subject)
    if subject:
        subject.count_of_tasks += 1
        await db.commit()
    return task

async def update_task(db: AsyncSession, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[Task]:
    task = await get_task_by_id(db, task_id)
    if not task or task.id_user != user_id:
        return None
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    # Если задача была публичной, после редактирования отправляем на модерацию
    if task.status == TaskStatus.public:
        task.status = TaskStatus.draft
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task_by_author(db: AsyncSession, task_id: int, user_id: int) -> bool:
    task = await get_task_by_id(db, task_id)
    if not task or task.id_user != user_id:
        return False
    # Удалить связанные данные
    await db.execute(delete(TaskComment).where(TaskComment.id_task == task_id))
    await db.execute(delete(TaskRating).where(TaskRating.id_task == task_id))
    await db.execute(delete(ViewHistory).where(ViewHistory.id_task == task_id))
    await db.execute(delete(SolutionView).where(SolutionView.id_task == task_id))
    await db.delete(task)
    # Уменьшить счётчик
    subject = await db.get(Subject, task.id_subject)
    if subject:
        subject.count_of_tasks = max(0, subject.count_of_tasks - 1)
    await db.commit()
    return True

# ---------- Views ----------
async def add_page_view(db: AsyncSession, user_id: int, task_id: int):
    # Проверяем, существует ли уже запись для этого пользователя и задачи
    existing = await db.execute(
        select(ViewHistory).where(
            ViewHistory.id_user == user_id,
            ViewHistory.id_task == task_id
        )
    )
    if not existing.scalar_one_or_none():
        view = ViewHistory(id_user=user_id, id_task=task_id)
        db.add(view)
        await db.commit()

async def add_solution_view(db: AsyncSession, user_id: int, task_id: int):
    existing = await db.execute(
        select(SolutionView).where(
            SolutionView.id_user == user_id,
            SolutionView.id_task == task_id
        )
    )
    if not existing.scalar_one_or_none():
        view = SolutionView(id_user=user_id, id_task=task_id)
        db.add(view)
        await db.commit()

async def get_unique_page_views(db: AsyncSession, task_id: int) -> int:
    result = await db.execute(
        select(func.count()).select_from(ViewHistory).where(ViewHistory.id_task == task_id)
    )
    return result.scalar_one()

async def get_unique_solution_views(db: AsyncSession, task_id: int) -> int:
    result = await db.execute(
        select(func.count()).select_from(SolutionView).where(SolutionView.id_task == task_id)
    )
    return result.scalar_one()

# ---------- Ratings ----------
async def get_average_rating(db: AsyncSession, task_id: int) -> Optional[float]:
    result = await db.execute(
        select(func.avg(TaskRating.rating)).where(TaskRating.id_task == task_id)
    )
    avg = result.scalar()
    return round(avg, 2) if avg else None

async def get_user_rating(db: AsyncSession, task_id: int, user_id: int) -> Optional[TaskRating]:
    result = await db.execute(
        select(TaskRating).where(
            TaskRating.id_task == task_id,
            TaskRating.id_user == user_id
        )
    )
    return result.scalar_one_or_none()

async def create_rating(db: AsyncSession, task_id: int, user_id: int, rating_value: int) -> TaskRating:
    rating = TaskRating(id_task=task_id, id_user=user_id, rating=rating_value)
    db.add(rating)
    await db.commit()
    await db.refresh(rating)
    return rating

async def update_rating(db: AsyncSession, rating_id: int, rating_value: int) -> TaskRating:
    rating = await db.get(TaskRating, rating_id)
    if rating:
        rating.rating = rating_value
        await db.commit()
        await db.refresh(rating)
    return rating

# ---------- Comments ----------
async def get_comments_count(db: AsyncSession, task_id: int) -> int:
    result = await db.execute(
        select(func.count()).select_from(TaskComment).where(
            TaskComment.id_task == task_id,
            TaskComment.status == "active"
        )
    )
    return result.scalar_one()

async def get_task_comments(db: AsyncSession, task_id: int) -> List[TaskComment]:
    result = await db.execute(
        select(TaskComment)
        .options(joinedload(TaskComment.user))
        .where(TaskComment.id_task == task_id, TaskComment.status == "active")
        .order_by(TaskComment.id_task_comment)
    )
    return result.unique().scalars().all()

async def create_comment(db: AsyncSession, task_id: int, user_id: int, comment_text: str) -> TaskComment:
    comment = TaskComment(
        id_task=task_id,
        id_user=user_id,
        comment=comment_text,
        status="active"
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment

# ---------- Stats for author ----------
async def get_tasks_by_author(db: AsyncSession, author_id: int) -> List[Task]:
    result = await db.execute(
        select(Task).where(Task.id_user == author_id, Task.status == "active")
    )
    return result.scalars().all()

async def get_rating_stats(db: AsyncSession, task_id: int) -> tuple[int, Optional[float]]:
    count_res = await db.execute(
        select(func.count()).select_from(TaskRating).where(TaskRating.id_task == task_id)
    )
    count = count_res.scalar_one()
    avg_res = await db.execute(
        select(func.avg(TaskRating.rating)).where(TaskRating.id_task == task_id)
    )
    avg = avg_res.scalar()
    return count, round(avg, 2) if avg else None

async def get_all_tasks_for_moderator(
    db: AsyncSession,
    status_filter: Optional[TaskStatus] = None,
    skip: int = 0,
    limit: int = 50
) -> List[Task]:
    query = select(Task).options(
        joinedload(Task.subject),
        joinedload(Task.author)
    )
    if status_filter:
        query = query.where(Task.status == status_filter)
    query = query.order_by(Task.updated_at.desc(), Task.id_task.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.unique().scalars().all()

async def update_task_status(db: AsyncSession, task_id: int, new_status: TaskStatus) -> Optional[Task]:
    task = await db.get(Task, task_id)
    if not task:
        return None
    task.status = new_status
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task_moderator(db: AsyncSession, task_id: int) -> bool:
    task = await db.get(Task, task_id)
    if not task:
        return False
    # Удаляем связанные данные (как при удалении автором)
    await db.execute(delete(TaskComment).where(TaskComment.id_task == task_id))
    await db.execute(delete(TaskRating).where(TaskRating.id_task == task_id))
    await db.execute(delete(ViewHistory).where(ViewHistory.id_task == task_id))
    await db.execute(delete(SolutionView).where(SolutionView.id_task == task_id))
    await db.delete(task)
    # Корректируем счётчик задач в предмете
    subject = await db.get(Subject, task.id_subject)
    if subject:
        subject.count_of_tasks = max(0, subject.count_of_tasks - 1)
    await db.commit()
    return True

# ---------- Модерация комментариев ----------
async def get_all_comments_for_moderator(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50
) -> List[TaskComment]:
    query = select(TaskComment).options(
        joinedload(TaskComment.user),
        joinedload(TaskComment.task).joinedload(Task.subject)
    ).order_by(TaskComment.id_task_comment.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.unique().scalars().all()

async def delete_comment_moderator(db: AsyncSession, comment_id: int) -> bool:
    comment = await db.get(TaskComment, comment_id)
    if not comment:
        return False
    # Можно физически удалить или пометить deleted
    await db.delete(comment)
    await db.commit()
    return True

# ---------- Управление пользователями (модератор/админ) ----------

async def get_user_by_email_for_action(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(
        select(User)
        .options(selectinload(User.role))  # 👈 важно
        .where(User.email == email)
    )
    return result.scalar_one_or_none()

async def soft_delete_user_by_email(db: AsyncSession, email: str) -> bool:
    user = await get_user_by_email_for_action(db, email)
    if not user or user.is_deleted:
        return False
    # Модератор не может удалять админов и модераторов
    role = user.role.role_name if user.role else None
    if role in ["admin", "moderator"]:
        return False
    await soft_delete_user(db, user)
    return True

async def get_all_users_admin(db: AsyncSession) -> List[User]:
    result = await db.execute(
        select(User).options(joinedload(User.role)).order_by(User.id_user)
    )
    return result.unique().scalars().all()

async def change_user_role(db: AsyncSession, user_id: int, new_role_name: str) -> Optional[User]:
    user = await db.get(User, user_id)
    if not user:
        return None
    role_res = await db.execute(select(Role).where(Role.role_name == new_role_name))
    role = role_res.scalar_one_or_none()
    if not role:
        return None
    user.id_role = role.id_role
    await db.commit()
    await db.refresh(user)
    return user