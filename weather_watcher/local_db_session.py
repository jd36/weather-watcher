from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from weather_watcher.config import settings

BASE = declarative_base()
ENGINE = create_engine(settings.MYSQL_DATABASE_URI.unicode_string())
LOCAL_DB_SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
