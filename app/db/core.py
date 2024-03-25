from sqlalchemy import Integer, and_, func, insert, select, text, update
from sqlalchemy.orm import aliased

from app.db.database import sync_engine
from app.db.models import metadata, users_table, desks_table, tasks_table, status_table


def add_roles():
    with sync_engine.connect() as conn:
        stmt = insert(status_table).values(
            [
                {"status_name": "user"},
                {"status_name": "manager"},
                {"status_name": "admin"}
            ]
        )
        conn.execute(stmt)
        conn.commit()


def create_tables():
    metadata.drop_all(sync_engine)

    metadata.create_all(sync_engine)

    add_roles()


def insert_user(login, password, name, role):
    with sync_engine.connect() as conn:
        stmt = insert(users_table).values(
            [
                {"login": login, "hash_pass": password, "name": name, "role": role}
            ]
        )
        conn.execute(stmt)
        conn.commit()


def pass_for_login(login):
    with (sync_engine.connect() as conn):
        stmt = (
            select(
                users_table.c.hash_pass
            )
            .select_from(users_table)
            .filter(users_table.c.login == login
                    )
        )
        res = conn.execute(stmt)
        conn.commit()
        return res.first()


def create_new_desk(desk_name, invite_code, admin_id, description):
    with sync_engine.connect() as conn:
        stmt = insert(desks_table).values(
            [
                {"desk_name": desk_name, "invite_code": invite_code, "admin_id": admin_id, "description": description}
            ]
        )
        conn.execute(stmt)
        conn.commit()


def create_new_task(desk_id, task_name, description, creator_id, status_id, creation_date, deadline):
    with sync_engine.connect() as conn:
        stmt = insert(tasks_table).values(
            [
                {"desk_id": desk_id,
                 "task_name": task_name,
                 "description": description,
                 "creator_id": creator_id,
                 "status_id": status_id,
                 "creation_date": creation_date,
                 "deadline": deadline}
            ]
        )
        conn.execute(stmt)
        conn.commit()
