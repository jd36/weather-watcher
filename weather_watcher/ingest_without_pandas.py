import os
import time
from glob import glob
from weather_watcher.local_db_session import LOCAL_DB_SESSION
from weather_watcher.models import WeatherStation, WeatherMeasurement


# ------------------------------
# ---        CONSTANTS       ---
# ------------------------------
FILES_TO_INGEST = "wx_data/*.txt"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DIRECTORY = FILES_TO_INGEST.split("/")[0]
FILE_EXTENSION = FILES_TO_INGEST.split(".")[1]


# ******************************
# ***   PRINTING Functions   ***
# ******************************
def print_log(message):
    print(f"--- LOG: {message} ---")


def print_time(time_description):
    time_output = time.time()
    time_log = time.strftime(TIME_FORMAT, time.localtime(time_output))
    print_log(f"{time_description} time: {time_log}")
    return time_output


def print_end_logs(start_time, total_records_ingested):
    end_time = print_time("  end")
    print_log(f"execution time: {end_time - start_time} seconds")
    print_log(f"number of rows inserted: {total_records_ingested}")


# ++++++++++++++++++++++++++++++
# +++   DATABASE Functions   +++
# ++++++++++++++++++++++++++++++
def is_valid(measurement):
    return measurement != -9999


def process_weather_measurements(filename, db):
    total_records_ingested = 0
    station_name = filename.split("/")[1].split(".")[0]
    # Check if weather station name already exists in the weather_station table
    weather_station = (
        db.query(WeatherStation).filter(WeatherStation.name == station_name).first()
    )
    print_log(f"weather station = {station_name}")
    if weather_station is None:
        # Blank means the weather station was not found in the table, so add it
        weather_station = WeatherStation(name=station_name)
        db.add(weather_station)
        db.flush()

        # Open data file, loop through the file, one line at a time
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                # Parse each line in the file and place the data into the model
                for line in file:
                    # Split the line by tab character
                    data = line.strip().split("\t")
                    weather_measurement = WeatherMeasurement(
                        station_id=weather_station.id,
                        date=data[0],
                        max_temperature=int(data[1]) / 10
                        if is_valid(int(data[1]))
                        else None,
                        min_temperature=int(data[2]) / 10
                        if is_valid(int(data[2]))
                        else None,
                        precipitation=int(data[3]) / 10000
                        if is_valid(int(data[3]))
                        else None,
                    )
                    # Insert data via model into DB table
                    db.add(weather_measurement)
                    total_records_ingested = total_records_ingested + 1
        db.commit()
    print_log(f"   number records ingested = {total_records_ingested}")
    return total_records_ingested


def ingest_weather_files():
    start_time = print_time("start")
    total_records_ingested = 0
    with LOCAL_DB_SESSION() as db:
        for filename in glob(FILES_TO_INGEST):
            total_records_ingested = (
                total_records_ingested + process_weather_measurements(filename, db)
            )
    print_end_logs(start_time, total_records_ingested)


if __name__ == "__main__":
    ingest_weather_files()
