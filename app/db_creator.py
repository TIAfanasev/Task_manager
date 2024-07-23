from app.db.core import create_tables
from app.routes.test_data import create_test_data
from app.db.database import sync_engine

from sqlalchemy_utils import database_exists, create_database

if __name__ == '__main__':
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)
    create_tables()
    create_test_data()
