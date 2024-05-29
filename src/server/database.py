import sqlite3
import os
from fastapi.responses import JSONResponse

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

current_dir = os.getcwd()
path_db = os.path.join(current_dir, 'tables.db')


engine = create_engine(
    "sqlite:///tables.db", echo=True, echo_pool="debug",
    connect_args={"check_same_thread": False}
)

@event.listens_for(engine, "connect")
def set_foreign_keys_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
