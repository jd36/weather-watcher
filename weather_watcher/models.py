from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from weather_watcher.local_db_session import BASE


class WeatherMeasurement(BASE):
    __tablename__ = "weather_measurements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("weather_stations.id"), nullable=False)
    date = Column(Date, nullable=False)
    max_temperature = Column(Float, nullable=True)
    min_temperature = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)


class WeatherStatistic(BASE):
    __tablename__ = "weather_statistics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("weather_stations.id"), nullable=False)
    year = Column(Integer, nullable=False)
    avg_max_temperature = Column(Float, nullable=True)
    avg_min_temperature = Column(Float, nullable=True)
    total_precipitation = Column(Float, nullable=True)


class WeatherStation(BASE):
    __tablename__ = "weather_stations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    weather_measurements = relationship(WeatherMeasurement, backref="weather_stations")
    weather_statistics = relationship(WeatherStatistic, backref="weather_stations")


if __name__ == "__main__":
    print("Map to tables", BASE.metadata.tables)
