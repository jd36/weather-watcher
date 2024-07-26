"""create weather measurements table

Revision ID: c4e42f290324
Revises: 77b93e44bed4
Create Date: 2024-07-23 01:02:24.908527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c4e42f290324"
down_revision: Union[str, None] = "77b93e44bed4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.DDL(
            """
        CREATE TABLE IF NOT EXISTS weather_measurements (
            id INT AUTO_INCREMENT NOT NULL,
            station_id INT NOT NULL,
            date DATE NOT NULL,
            max_temperature FLOAT,
            min_temperature FLOAT,
            precipitation FLOAT,
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
        DROP TABLE weather_measurements;
        """
        )
    )
