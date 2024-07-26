from sqlalchemy import text
from weather_watcher.local_db_session import LOCAL_DB_SESSION


CLEAN_SQL = """
    TRUNCATE TABLE weather_statistics;
"""

COMPUTE_SQL = """
    INSERT INTO weather_statistics (
        station_id,
        year,
        avg_max_temperature,
        avg_min_temperature,
        total_precipitation)
    SELECT
        station_id,
        YEAR(date) as year,
        AVG(max_temperature) as avg_max_temperature,
        AVG(min_temperature) as avg_min_temperature,
        SUM(precipitation) as total_precipitation
    FROM weather_measurements
    GROUP BY station_id, year;
"""


def compute_statistics():
    with LOCAL_DB_SESSION() as db:
        # Remove all data in stats table before inserting computed data
        db.execute(text(CLEAN_SQL))
        db.execute(text(COMPUTE_SQL))
        db.commit()


if __name__ == "__main__":
    compute_statistics()
