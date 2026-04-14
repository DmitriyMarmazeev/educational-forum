from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum

# ---------- User ----------
class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str

class UserCreate(UserBase):
    password: str

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id_user: int
    wallet: Optional[str] = None
    subscribed_until_date: Optional[datetime] = None
    role_name: str = Field(alias="role_name")   # из join

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserProfileOut(BaseModel):
    id_user: int
    name: str
    surname: str
    role_name: str
    is_deleted: bool = False

    model_config = ConfigDict(from_attributes=True)

# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

# ---------- Subject ----------
class SubjectBase(BaseModel):
    subject_name: str

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase):
    id_subject: int
    count_of_tasks: int

    model_config = ConfigDict(from_attributes=True)

# ---------- Task ----------
class TaskStatusEnum(str, Enum):
    draft = "draft"
    public = "public"
    rejected = "rejected"
    archived = "archived"

class TaskBase(BaseModel):
    condition: str
    image: Optional[str] = None
    answer: str
    task_number: int
    id_subject: int

class TaskCreate(TaskBase):
    solution: str   # при создании решение обязательно

class TaskUpdate(BaseModel):
    condition: Optional[str] = None
    image: Optional[str] = None
    solution: Optional[str] = None
    answer: Optional[str] = None
    task_number: Optional[int] = None
    id_subject: Optional[int] = None

class TaskOut(BaseModel):
    id_task: int
    condition: str
    image: Optional[str] = None
    answer: str
    task_number: int
    status: TaskStatusEnum
    author_name: Optional[str] = None      # "Удалённый аккаунт" если автор удалён
    subject_name: str
    average_rating: Optional[float] = None
    comments_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class TaskSolutionOut(BaseModel):
    solution: str

    model_config = ConfigDict(from_attributes=True)


class TaskDetailOut(TaskOut):
    solution: Optional[str] = None   # показывается только если есть подписка

# ---------- Rating ----------
class RatingCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)

class RatingOut(BaseModel):
    id_task_rating: int
    rating: int
    id_task: int
    user_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# ---------- Comment ----------
class CommentCreate(BaseModel):
    comment: str

class CommentOut(BaseModel):
    id_task_comment: int
    comment: str
    status: str
    created_at: Optional[datetime] = None   # добавим в модель поле даты? По желанию
    user_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# ---------- Stats ----------
class TaskStatsOut(BaseModel):
    id_task: int
    unique_views: int
    solution_views: int
    ratings_count: int
    average_rating: Optional[float]


class ChangeRoleRequest(BaseModel):
    role_name: str

# Схема удаления пользователя по email
class DeleteUserByEmailRequest(BaseModel):
    email: EmailStr

class CommentModeratorOut(BaseModel):
    id_task_comment: int
    comment: str
    task_id: int
    user_id: int
    user_email: Optional[str] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class TaskModeratorOut(TaskOut):
    author_id: int
    author_email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None