"""create weather statistics table

Revision ID: 7deea2458c46
Revises: c4e42f290324
Create Date: 2024-07-23 01:04:17.329424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7deea2458c46"
down_revision: Union[str, None] = "c4e42f290324"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.DDL(
            """
        CREATE TABLE IF NOT EXISTS weather_statistics (
            id INT AUTO_INCREMENT NOT NULL,
            station_id INT NOT NULL,
            year INT NOT NULL,
            avg_max_temperature FLOAT,
            avg_min_temperature FLOAT,
            total_precipitation FLOAT,
            PRIMARY KEY (id),
            FOREIGN KEY (station_id)
                REFERENCES weather_stations(id)
        ) ENGINE=InnoDB;
        """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.DDL(
            """
        DROP TABLE weather_statistics;
        """
        )
    )
