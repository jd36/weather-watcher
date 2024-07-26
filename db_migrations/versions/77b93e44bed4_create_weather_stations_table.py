"""create weather stations table

Revision ID: 77b93e44bed4
Revises:
Create Date: 2024-07-20 18:47:27.702361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "77b93e44bed4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.DDL(
            """
        CREATE TABLE IF NOT EXISTS weather_stations (
            id INT AUTO_INCREMENT NOT NULL,
            name CHAR(255) NOT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY unique_name (name)
        ) ENGINE=InnoDB;
        """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.DDL(
            """
        DROP TABLE weather_stations;
        """
        )
    )
