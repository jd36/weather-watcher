from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from weather_watcher.local_db_session import LOCAL_DB_SESSION


def get_db_connection():
    db = LOCAL_DB_SESSION()
    try:
        yield db
    finally:
        db.close()


DB_SESSION = Annotated[Session, Depends(get_db_connection)]
