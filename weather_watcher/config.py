from typing import Any, Optional
from pydantic import MySQLDsn, field_validator
from pydantic_settings import BaseSettings
from pydantic_core.core_schema import ValidationInfo


class Settings(BaseSettings):
    MYSQL_SERVER: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_DATABASE_URI: Optional[MySQLDsn] = None

    @field_validator("MYSQL_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return MySQLDsn.build(
            scheme="mysql",
            username=values.data.get("MYSQL_USER"),
            password=values.data.get("MYSQL_PASSWORD"),
            host=values.data.get("MYSQL_SERVER"),
            path=f"{values.data.get('MYSQL_DATABASE') or ''}",
        )


settings = Settings()
