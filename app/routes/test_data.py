from fastapi import APIRouter
from app.db.database import session_factory
from app.db.models import (
    UsersTable,
    DesksTable,
    TasksTable,
    UsersTasksTable
)

router = APIRouter()


def create_test_data():
    with session_factory() as session:
        user1 = UsersTable(login='user',
                           hash_pass='950d36187c975bbc97adcdb248dcc2c5',
                           name='Boris',
                           role=3)
        user2 = UsersTable(login='user2',
                           hash_pass='950d36187c975bbc97adcdb248dcc2c5',
                           name='Vova',
                           role=2)
        session.add(user1)
        session.commit()
        desk1 = DesksTable(desk_name="desk1",
                           invite_code="qfv2vjenov4nfd2hd0",
                           admin_id=1,
                           description="test desk")
        desk2 = DesksTable(desk_name="desk2",
                           invite_code="gjsvnur83ndis",
                           admin_id=1,
                           description="test desk")

        task1 = TasksTable(desk_id=1,
                           task_name="task1",
                           description="descr_of_the_task",
                           creator_id=1,
                           status_id=1,
                           creation_date="2001-08-22",
                           deadline="2024-08-22")
        task2 = TasksTable(desk_id=2,
                           task_name="task2",
                           description="descr_of_the_task",
                           creator_id=1,
                           status_id=1,
                           creation_date="2001-08-22",
                           deadline="2024-08-22")

        conn1 = UsersTasksTable(user_id=1, task_id=1)
        conn2 = UsersTasksTable(user_id=1, task_id=2)
        session.add_all([desk1, desk2, task1, task2, conn1, conn2])

        session.commit()
