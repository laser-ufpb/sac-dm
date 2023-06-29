import sqlite3
import os
from fastapi.responses import JSONResponse

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

current_dir = os.getcwd()
path_db = os.path.join(current_dir, 'tables.db')


engine = create_engine(
    "sqlite:///tables.db", echo=True,
    connect_args={"check_same_thread": False}
)

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


# Function to get all data from device table
def get_all_data():
    try:
        with sqlite3.connect(path_db) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM device")
            data = c.fetchall()
            return data
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))
