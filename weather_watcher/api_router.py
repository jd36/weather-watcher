from fastapi import APIRouter
from typing import List, Optional
from sqlalchemy.orm import joinedload
from weather_watcher.db_session import DB_SESSION
from weather_watcher.models import WeatherStation, WeatherMeasurement, WeatherStatistic
from weather_watcher.schemas import (
    WeatherStationsSchema,
    WeatherMeasurementsSchema,
    WeatherStatisticsSchema,
)


router = APIRouter()


@router.get(
    "/weather/stations",
    response_model=List[WeatherStationsSchema],
    response_description="Weather Stations",
)
async def get_weather_stations(db: DB_SESSION, offset: int = 0, limit: int = 20):
    stations = (
        db.query(WeatherStation)
        .order_by(WeatherStation.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    response = [
        WeatherStationsSchema(id=station.id, name=station.name) for station in stations
    ]
    return response


@router.get(
    "/weather/",
    response_model=List[WeatherMeasurementsSchema],
    response_description="Weather Measurements",
)
async def get_weather_measurements(
    db: DB_SESSION,
    date: Optional[str] = None,
    station_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 20,
):
    measurements = ()
    if date is not None:
        if station_id is not None:
            # Run query with provided filters for date and station_id
            measurements = (
                db.query(WeatherMeasurement)
                .filter(WeatherMeasurement.date == date)
                .filter(WeatherMeasurement.station_id == station_id)
                .options(joinedload(WeatherMeasurement.weather_stations))
                .order_by(WeatherMeasurement.id)
                .offset(offset)
                .limit(limit)
                .all()
            )
        else:
            # Run query with provided filter for date
            measurements = (
                db.query(WeatherMeasurement)
                .filter(WeatherMeasurement.date == date)
                .options(joinedload(WeatherMeasurement.weather_stations))
                .order_by(WeatherMeasurement.id)
                .offset(offset)
                .limit(limit)
                .all()
            )
    else:
        if station_id is not None:
            # Run query with provided filter for station_id
            measurements = (
                db.query(WeatherMeasurement)
                .filter(WeatherMeasurement.station_id == station_id)
                .options(joinedload(WeatherMeasurement.weather_stations))
                .order_by(WeatherMeasurement.id)
                .offset(offset)
                .limit(limit)
                .all()
            )
        else:
            # Run query without any filters
            measurements = (
                db.query(WeatherMeasurement)
                .options(joinedload(WeatherMeasurement.weather_stations))
                .order_by(WeatherMeasurement.id)
                .offset(offset)
                .limit(limit)
                .all()
            )

    response = [
        WeatherMeasurementsSchema(
            id=measurement.id,
            station_name=measurement.weather_stations.name,
            date=str(measurement.date),
            max_temperature=measurement.max_temperature,
            min_temperature=measurement.min_temperature,
            precipitation=measurement.precipitation,
        )
        for measurement in measurements
    ]
    return response


@router.get(
    "/weather/stats",
    response_model=List[WeatherStatisticsSchema],
    response_description="Weather Statistics",
)
async def get_weather_statistics(
    db: DB_SESSION,
    year: Optional[int] = None,
    station_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 20,
):
    statistics = ()
    if year is not None:
        if station_id is not None:
            # Run query with provided filters for date and station_id
            statistics = (
                db.query(WeatherStatistic)
                .filter(WeatherStatistic.year == year)
                .filter(WeatherStatistic.station_id == station_id)
                .options(joinedload(WeatherStatistic.weather_stations))
                .order_by(WeatherStatistic.id)
                .offset(offset)
                .limit(limit)
                .all()
            )
        else:
            # Run query with provided filter for year
            statistics = (
                db.query(WeatherStatistic)
                .filter(WeatherStatistic.year == year)
                .options(joinedload(WeatherStatistic.weather_stations))
                .order_by(WeatherStatistic.id)
                .offset(offset)
                .limit(limit)
                .all()
            )
    else:
        if station_id is not None:
            # Run query with provided filter station_id
            statistics = (
                db.query(WeatherStatistic)
                .filter(WeatherStatistic.station_id == station_id)
                .options(joinedload(WeatherStatistic.weather_stations))
                .order_by(WeatherStatistic.id)
                .offset(offset)
                .limit(limit)
                .all()
            )
        else:
            # Run query without any provided filters
            statistics = (
                db.query(WeatherStatistic)
                .options(joinedload(WeatherStatistic.weather_stations))
                .order_by(WeatherStatistic.id)
                .offset(offset)
                .limit(limit)
                .all()
            )

    response = [
        WeatherStatisticsSchema(
            id=stat.id,
            station_name=stat.weather_stations.name,
            year=str(stat.year),
            avg_max_temperature=stat.avg_max_temperature,
            avg_min_temperature=stat.avg_min_temperature,
            total_precipitation=stat.total_precipitation,
        )
        for stat in statistics
    ]
    return response
