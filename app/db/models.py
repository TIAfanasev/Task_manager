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
    Date
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, unique=True),
    Column("hash_pass", String),
    Column("name", String),
    Column("role", Integer)
)

desks_table = Table(
    "desks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("desk_name", String, unique=True),
    Column("invite_code", String, unique=True),
    Column("admin_id", Integer),
    Column("description", String)
)

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

status_table = Table(
    "status",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("status_name", String, unique=True)
)

users_tasks_table = Table(
    "users_tasks",
    metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("desk_id", Integer, ForeignKey("desks.id", ondelete="CASCADE"))
)

