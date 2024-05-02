from sqlalchemy import Integer, and_, func, insert, select, text, update, delete
from sqlalchemy.orm import aliased
from typing import List

from app.db.database import sync_engine, session_factory, Base
from app.db.models import (
    UsersTable,
    DesksTable,
    TasksTable,
    StatusTable,
    UsersTasksTable,
    RoleTable
)
import app.models.models as md


def add_roles_and_statuses():
    with session_factory() as session:
        user = RoleTable(role_name="user")
        manager = RoleTable(role_name="manager")
        admin = RoleTable(role_name="admin")
        created = StatusTable(status_name="created")
        in_process = StatusTable(status_name="in process")
        completed = StatusTable(status_name="completed")
        session.add_all([user, manager, admin, created, in_process, completed])
        session.commit()


def create_tables():
    Base.metadata.drop_all(sync_engine)

    Base.metadata.create_all(sync_engine)

    add_roles_and_statuses()


def insert_user(log, password, name, role):
    with session_factory() as session:
        user = UsersTable(login=log, hash_pass=password, name=name, role=role)
        session.add(user)
        session.commit()


def pass_for_login(login):
    with session_factory() as session:
        users_pass = session.query(UsersTable.hash_pass).filter(UsersTable.login == login).scalar()
        print(users_pass)
        return users_pass


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
        delete_old_users = delete(UsersTasksTable).where(UsersTasksTable.task_id == task_id)
        session.execute(delete_old_users)
        users = []
        for x in user_list:
            users.append(UsersTasksTable(user_id=x.id, task_id=task_id))
        session.add_all(users)
        session.commit()


def get_user_from_db(username: str):
    with session_factory() as session:
        user = session.query(UsersTable).filter(UsersTable.login == username).one()
        return user.id, user.role


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


def get_all_tasks_for_desk(desk_id: int) -> list[md.TasksInfoForOneDesk]:
    with (session_factory() as session):
        full_tasks = session.query(TasksTable.id,
                                   TasksTable.desk_id,
                                   TasksTable.task_name,
                                   TasksTable.description,
                                   TasksTable.creator_id,
                                   TasksTable.status_id,
                                   TasksTable.creation_date,
                                   TasksTable.deadline
                                   ).filter(
            TasksTable.desk_id == desk_id
        ).all()
        print(full_tasks)
        tasks_with_users = []
        for one_task in full_tasks:
            users_info = get_users_info(one_task[0])
            users_info = [md.UserInfo(id=i[0], login=i[1], name=i[2], role=i[3]) for i in users_info]
            tasks_with_users.append(md.TasksInfoForOneDesk(id=one_task[0],
                                                           desk_id=one_task[1],
                                                           task_name=one_task[2],
                                                           description=one_task[3],
                                                           creator_id=one_task[4],
                                                           status_id=one_task[5],
                                                           creation_date=one_task[6],
                                                           deadline=one_task[7],
                                                           users_list=users_info
                                                           ))
        return tasks_with_users


def get_users_info(task_id: int) -> list[md.UserInfo]:
    with (session_factory() as session):
        users_list_id = session.query(UsersTasksTable.user_id).filter(UsersTasksTable.task_id == task_id).all()
        user_info_list = []
        for user in users_list_id:
            if user[0]:
                user_info = session.query(UsersTable.id, UsersTable.login, UsersTable.name, UsersTable.role
                                          ).filter(UsersTable.id == user[0]).one_or_none()
                user_info_list.append(user_info)
        return user_info_list


def add_tokens(user_id: int, a_token: str, r_token: str):
    with (session_factory() as session):
        user = update(UsersTable
                      ).where(UsersTable.id == user_id
                              ).values(access_token=a_token, refresh_token=r_token)
        session.execute(user)
        session.commit()


# type == 1 if access token check n type == 0 if refresh token check
def get_user_tokens(token_type: bool, user_id: int):
    with (session_factory() as session):
        if token_type:
            field = UsersTable.access_token
        else:
            field = UsersTable.refresh_token
        token = session.query(field).filter(UsersTable.id == user_id).one_or_none()
        return token[0]


def get_desk_info(desk_id: int):
    with session_factory() as session:
        desk_info = session.query(DesksTable.id,
                                  DesksTable.desk_name,
                                  DesksTable.invite_code,
                                  DesksTable.admin_id,
                                  DesksTable.description).filter(DesksTable.id == desk_id).one()
        all_tasks = session.query(TasksTable.id).where(TasksTable.desk_id == desk_id).all()
        all_tasks_list = []
        for x in all_tasks:
            all_tasks_list.append(get_task_info(x[0]))
        desk_info_result = md.FullDeskInfo(id=desk_info[0],
                                           desk_name=desk_info[1],
                                           invite_code=desk_info[2],
                                           admin_id=desk_info[3],
                                           description=desk_info[4],
                                           tasks_list=all_tasks_list)

        return desk_info_result


def get_user_info(user_id: int):
    with session_factory() as session:
        user_info = session.query(UsersTable.id,
                                  UsersTable.login,
                                  UsersTable.hash_pass,
                                  UsersTable.name,
                                  UsersTable.role).filter(UsersTable.id == user_id).one()
        return user_info


def update_desk_info(desk):
    with session_factory() as session:
        desk_update = update(DesksTable
                             ).where(DesksTable.id == desk['id']
                                     ).values(desk_name=desk['desk_name'],
                                              admin_id=desk['admin_id'],
                                              description=desk['description'])
        session.execute(desk_update)
        session.commit()
        return desk['id']


def update_user_info(user):
    with session_factory() as session:
        user_update = update(UsersTable
                             ).where(UsersTable.id == user['id']
                                     ).values(login=user['login'],
                                              hash_pass=user['hash_pass'],
                                              name=user['name'],
                                              role=user["role"])
        session.execute(user_update)
        session.commit()


def delete_one_desk(desk_id):
    with session_factory() as session:
        delete_task = delete(DesksTable).where(DesksTable.id == desk_id)
        session.execute(delete_task)
        session.commit()


def delete_one_user(user_id):
    with session_factory() as session:
        delete_user = delete(UsersTable).where(UsersTable.id == user_id)
        session.execute(delete_user)
        session.commit()


def get_task_info(task_id):
    with (session_factory() as session):
        full_task = session.query(TasksTable.id,
                                  TasksTable.desk_id,
                                  TasksTable.task_name,
                                  TasksTable.description,
                                  TasksTable.creator_id,
                                  TasksTable.status_id,
                                  TasksTable.creation_date,
                                  TasksTable.deadline
                                  ).filter(
            TasksTable.id == task_id
        ).one()
        users_info = get_users_info(full_task[0])
        users_info = [md.UserInfo(id=i[0], login=i[1], name=i[2], role=i[3]) for i in users_info]
        task_info = md.TasksInfoForOneDesk(id=full_task[0],
                                           desk_id=full_task[1],
                                           task_name=full_task[2],
                                           description=full_task[3],
                                           creator_id=full_task[4],
                                           status_id=full_task[5],
                                           creation_date=full_task[6],
                                           deadline=full_task[7],
                                           users_list=users_info)
        return task_info


def update_task_info(task):
    with session_factory() as session:
        task_update = update(TasksTable
                             ).where(TasksTable.id == task.id
                                     ).values(task_name=task.task_name,
                                              description=task.description,
                                              status_id=task.status_id,
                                              deadline=task.deadline)
        session.execute(task_update)
        session.commit()
        users_in_task(task_id=task.id, user_list=task.users_list)
        return task.id


def delete_one_task(task_id: int):
    with session_factory() as session:
        delete_task = delete(TasksTable).where(TasksTable.id == task_id)
        session.execute(delete_task)
        session.commit()
