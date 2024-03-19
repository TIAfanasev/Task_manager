from sqlalchemy import Integer, and_, func, insert, select, text, update
from sqlalchemy.orm import aliased

from app.db.database import sync_engine
from app.db.models import metadata, users_table


def create_tables():
    metadata.drop_all(sync_engine)

    metadata.create_all(sync_engine)


def insert_user(login, password, name, role):
    with sync_engine.connect() as conn:
        stmt = insert(users_table).values(
            [
                {"login": login, "hash_pass": password, "name": name, "role": role}
            ]
        )
        conn.execute(stmt)
        conn.commit()
