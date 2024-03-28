from sqlalchemy import Integer, and_, func, insert, select, text, update
from sqlalchemy.orm import aliased

from app.db.database import sync_engine, session_factory, Base
from app.db.models import (
    UsersTable,
    DesksTable,
    TasksTable,
    StatusTable,
    UsersTasksTable
)
import app.models.models as md


def add_roles():
    with session_factory() as session:
        user = StatusTable(status_name="user")
        manager = StatusTable(status_name="manager")
        admin = StatusTable(status_name="admin")
        session.add_all([user, manager, admin])
        session.commit()


def create_tables():
    Base.metadata.drop_all(sync_engine)

    Base.metadata.create_all(sync_engine)

    add_roles()


def insert_user(log, password, name, role):
    with session_factory() as session:
        user = UsersTable(login=log, hash_pass=password, name=name, role=role)
        session.add(user)
        session.commit()


def pass_for_login(login):
    with session_factory() as session:
        user = session.query(UsersTable).filter(UsersTable.login == login).one()
        print(user.hash_pass)
        return user.hash_pass


def create_new_desk(desk_name, invite_code, admin_id, description):
    with session_factory() as session:
        desk = DesksTable(desk_name=desk_name,
                          invite_code=invite_code,
                          admin_id=admin_id,
                          description=description)
        session.add(desk)
        session.commit()


def create_new_task(desk_id, task_name, description, creator_id, status_id, creation_date, deadline):
    with session_factory() as session:
        task = TasksTable(desk_id=desk_id,
                          task_name=task_name,
                          description=description,
                          creator_id=creator_id,
                          status_id=status_id,
                          creation_date=creation_date,
                          deadline=deadline)
        session.add(task)
        session.commit()


def users_in_task(task_id, user_list):
    with session_factory() as session:
        users = []
        for x in user_list:
            users.append(UsersTasksTable(user_id=x, task_id=task_id))
        session.add_all(users)
        session.commit()


def get_user_from_db(username: str):
    with session_factory() as session:
        user = session.query(UsersTable).filter(UsersTable.login == username).one()
        return user.id


def get_all_tasks_for_user(user_id: int):
    with session_factory() as session:
        tasks_id = session.query(UsersTasksTable.task_id).filter(UsersTasksTable.user_id == user_id).order_by().all()
        all_tasks = set()
        for x in tasks_id:
            all_tasks.add(x[0])
        print("Vse taski ", all_tasks)
        return all_tasks


def get_desks_for_user(user_id: int):
    all_tasks = get_all_tasks_for_user(user_id)
    with session_factory() as session:
        desks_id = session.query(TasksTable.desk_id).filter(TasksTable.id.in_(all_tasks)).all()
        all_desks = set()
        for x in desks_id:
            all_desks.add(x[0])
        print("Vse deski", all_desks)

        desks = session.query(DesksTable.id, DesksTable.desk_name, DesksTable.invite_code, DesksTable.admin_id,
                              DesksTable.description).filter(DesksTable.id.in_(all_desks)).all()
        return desks


def get_most_important_tasks(user_id: int):
    all_tasks = get_all_tasks_for_user(user_id)
    with (session_factory() as session):
        tasks_info = session.query(TasksTable.id,
                                   TasksTable.desk_id,
                                   TasksTable.task_name,
                                   TasksTable.description,
                                   TasksTable.deadline
                                   ).filter(
                                    TasksTable.id.in_(all_tasks)
                                    ).limit(2).all()
        return tasks_info
