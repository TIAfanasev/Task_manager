import datetime
import enum
from typing import Annotated, Optional

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    text,
    Date,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

metadata = MetaData()

intpk = Annotated[int, mapped_column(primary_key=True)]


class UsersTable(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    login: Mapped[str] = mapped_column(unique=True)
    hash_pass: Mapped[str]
    name: Mapped[str]
    role: Mapped[int]


users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, unique=True),
    Column("hash_pass", String),
    Column("name", String),
    Column("role", Integer)
)


class DesksTable(Base):
    __tablename__ = "desks"

    id: Mapped[intpk]
    desk_name: Mapped[str] = mapped_column(unique=True)
    invite_code: Mapped[str] = mapped_column(unique=True)
    admin_id: Mapped[int]
    description: Mapped[str]


desks_table = Table(
    "desks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("desk_name", String, unique=True),
    Column("invite_code", String, unique=True),
    Column("admin_id", Integer),
    Column("description", String)
)


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


tasks_table = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("desk_id", Integer, ForeignKey("desks.id", ondelete="CASCADE")),
    Column("task_name", String, unique=True),
    Column("description", String),
    Column("creator_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("status_id", Integer, ForeignKey("status.id", ondelete="CASCADE")),
    Column("creation_date", Date),
    Column("deadline", Date)
)


class StatusTable(Base):
    __tablename__ = "status"

    id: Mapped[intpk]
    status_name: Mapped[str] = mapped_column(unique=True)


status_table = Table(
    "status",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("status_name", String, unique=True)
)


class UsersTasksTable(Base):
    __tablename__ = "users_tasks"
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(ForeignKey("desks.id", ondelete="CASCADE"))


users_tasks_table = Table(
    "users_tasks",
    metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("task_id", Integer, ForeignKey("desks.id", ondelete="CASCADE"))
)
