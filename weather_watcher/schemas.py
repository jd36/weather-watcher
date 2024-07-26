import pydantic
from fastapi import Body
from typing import Annotated


class WeatherStationsSchema(pydantic.BaseModel):
    id: Annotated[int, Body(description="Auto-incremented database ID")]
    name: Annotated[str, Body(description="Name of the weather station")]


class WeatherMeasurementsSchema(pydantic.BaseModel):
    id: Annotated[int, Body(description="Auto-incremented database ID")]
    station_name: Annotated[str, Body(description="Name of the weather station")]
    date: Annotated[str, Body(description="Date when the measurement was taken")]
    max_temperature: Annotated[
        float,
        Body(
            description="Maximum temperature in \
                                    degrees Celsius"
        ),
    ]
    min_temperature: Annotated[
        float,
        Body(
            description="Minimum temperature in \
                                    degrees Celsius"
        ),
    ]
    precipitation: Annotated[float, Body(description="Precipitation in centimeters")]


class WeatherStatisticsSchema(pydantic.BaseModel):
    id: Annotated[int, Body(description="Auto-incremented database ID")]
    station_name: Annotated[str, Body(description="Name of the weather station")]
    year: Annotated[
        int,
        Body(
            description="Year that the statistics \
                              represent"
        ),
    ]
    avg_max_temperature: Annotated[
        float,
        Body(
            description="Average maximum \
                                        temperature in degrees Celsius"
        ),
    ]
    avg_min_temperature: Annotated[
        float,
        Body(
            description="Average minimum \
                                        temperature in degrees Celsius"
        ),
    ]
    total_precipitation: Annotated[
        float,
        Body(
            description="Total precipitation in \
                                        centimeters"
        ),
    ]
