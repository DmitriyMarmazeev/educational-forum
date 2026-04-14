from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Numeric, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TaskStatus(str, enum.Enum):
    draft = "draft"
    public = "public"
    rejected = "rejected"
    archived = "archived"

class RoleEnum(str, enum.Enum):
    STUDENT = "student"
    AUTHOR = "author"
    ADMIN = "admin"
    MODERATOR = "moderator"   # на будущее

class Role(Base):
    __tablename__ = "roles"
    id_role = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    id_user = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    password = Column(String, nullable=False)   # хеш
    wallet = Column(String(100), nullable=True)      # заглушка для выплат
    subscribed_until_date = Column(DateTime(timezone=True), nullable=True)
    id_role = Column(Integer, ForeignKey("roles.id_role"), nullable=False)
    is_deleted = Column(Boolean, default=False)      # флаг удалённого аккаунта

    role = relationship("Role", back_populates="users")
    tasks = relationship("Task", back_populates="author", foreign_keys="Task.id_user")
    view_history = relationship("ViewHistory", back_populates="user")
    ratings = relationship("TaskRating", back_populates="user")
    comments = relationship("TaskComment", back_populates="user")
    solution_views = relationship("SolutionView", back_populates="user")

class Subject(Base):
    __tablename__ = "subjects"
    id_subject = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String(100), nullable=False, unique=True)
    count_of_tasks = Column(Integer, default=0)

    tasks = relationship("Task", back_populates="subject")

class Task(Base):
    __tablename__ = "tasks"
    id_task = Column(Integer, primary_key=True, index=True)
    condition = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)
    solution = Column(Text, nullable=True)           # видно только по подписке
    answer = Column(String(255), nullable=False)
    task_number = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.draft, nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    id_subject = Column(Integer, ForeignKey("subjects.id_subject"), nullable=False)

    author = relationship("User", back_populates="tasks", foreign_keys=[id_user])
    subject = relationship("Subject", back_populates="tasks")
    view_history = relationship("ViewHistory", back_populates="task")
    ratings = relationship("TaskRating", back_populates="task")
    comments = relationship("TaskComment", back_populates="task")
    solution_views = relationship("SolutionView", back_populates="task")

class ViewHistory(Base):
    __tablename__ = "view_history"
    id_view_history = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    id_task = Column(Integer, ForeignKey("tasks.id_task"), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)

    task = relationship("Task", back_populates="view_history")
    user = relationship("User", back_populates="view_history")

class SolutionView(Base):
    __tablename__ = "solution_views"
    id_solution_view = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    id_task = Column(Integer, ForeignKey("tasks.id_task"), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)


    task = relationship("Task", back_populates="solution_views")
    user = relationship("User", back_populates="solution_views")


class TaskRating(Base):
    __tablename__ = "task_rating"
    id_task_rating = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)  # например, от 1 до 5
    id_task = Column(Integer, ForeignKey("tasks.id_task"), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)

    task = relationship("Task", back_populates="ratings")
    user = relationship("User", back_populates="ratings")

class TaskComment(Base):
    __tablename__ = "task_comment"
    id_task_comment = Column(Integer, primary_key=True, index=True)
    comment = Column(Text, nullable=False)
    status = Column(String(50), default="active")   # active / deleted
    id_task = Column(Integer, ForeignKey("tasks.id_task"), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")