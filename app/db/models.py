import datetime
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class UsersTable(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    login: Mapped[str] = mapped_column(unique=True)
    hash_pass: Mapped[str]
    name: Mapped[str] = mapped_column(unique=True)
    role: Mapped[int] = mapped_column(ForeignKey("role.id", ondelete="CASCADE"))
    access_token: Mapped[str] = mapped_column(nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)


class DesksTable(Base):
    __tablename__ = "desks"

    id: Mapped[intpk]
    desk_name: Mapped[str] = mapped_column(unique=True)
    invite_code: Mapped[str] = mapped_column(unique=True)
    admin_id: Mapped[int]
    description: Mapped[str]


class TasksTable(Base):
    __tablename__ = "tasks"

    id: Mapped[intpk]
    desk_id: Mapped[int] = mapped_column(ForeignKey("desks.id", ondelete="CASCADE"))
    task_name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id", ondelete="CASCADE"))
    creation_date: Mapped[datetime.date] = mapped_column(default=datetime.date.today())
    deadline: Mapped[datetime.date]


class StatusTable(Base):
    __tablename__ = "status"

    id: Mapped[intpk]
    status_name: Mapped[str] = mapped_column(unique=True)


class RoleTable(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    role_name: Mapped[str] = mapped_column(unique=True)


class UsersTasksTable(Base):
    __tablename__ = "users_tasks"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))

