from fastapi import APIRouter
from app.db.database import session_factory
from app.db.models import (
    UsersTable,
    DesksTable,
    TasksTable,
    UsersTasksTable,
    StatusTable,
    RoleTable
)

router = APIRouter()


@router.post("/test_data")
async def create_test_data():
    with session_factory() as session:
        status1 = StatusTable(status_name="created")
        status2 = StatusTable(status_name="in process")
        status3 = StatusTable(status_name="completed")
        session.add_all([status1, status2, status3])

        role1 = RoleTable(role_name="user")
        role2 = RoleTable(role_name="manager")
        role3 = RoleTable(role_name="admin")
        session.add_all([role1, role2, role3])

        user = UsersTable(login='user1',
                          hash_pass='fn2oin02jc933d2sok',
                          name='Boris',
                          role=1)
        session.add(user)
        session.commit()

        desk1 = DesksTable(desk_name="desk1",
                           invite_code="qfv2vjenov4nfd2hd0",
                           admin_id=1,
                           description="test desk")
        desk2 = DesksTable(desk_name="desk2",
                           invite_code="gjsvnur83ndis",
                           admin_id=1,
                           description="test desk")
        session.add_all([desk1, desk2])

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
        session.add_all([task1, task2])

        conn1 = UsersTasksTable(user_id=1, task_id=1)
        conn2 = UsersTasksTable(user_id=1, task_id=2)
        session.add_all([conn1, conn2])

        session.commit()
