# ANSWERS

Steps on how to run the code for this exercise are after this answers section.

## Problem 1 - Data Modeling

The database I used for this coding exercise is MySQL Server v5.7.20 running inside a Docker container.  I used MySQL Workbench to design a data model and sketch out the ERD.  There are two files in `./answers/db_docs`.  

1. `DDL_Statements.txt` - contains the 3 DDL statements to create the 3 tables used in this exercise; one for the weather stations, one for the ingested measurements, and one for the statistics generated in the data analysis problem.
2. `WeatherWatcher_ERD.pdf` - shows the ERD for the WeatherWatcher database.

I made use of DDL statements using Alembic migrations in `./db_migrations`, but I also used SQLAlechmy ORM in my code.

## Problem 2 - Ingestion

I created two separate approaches to ingest the raw text files because I noticed the first approach seemed to run very slowly.  Both approaches took a long time to run.  Either way, all 167 raw data files were ingested, producing 1729957 records in the WeatherWatcher.weather_measurements table.

1. Using Pandas and data_frames in the file `./weather_watcher/ingest.py`, it took about 45 min.
2. Clearing the database and running the other script without using Pandas, but using os file and line by line reads in `./weather_watcher/ingest_without_pandas.py`, it actually took about 50 seconds longer. Re-running it after the database was populated, the script ingested 0 records in 0.56 second compared to the Pandas version, which took 12.42 seconds.  

As requested, I included the start time, end time, and number of records ingested in the console output as a result of running these ingestion scripts.  Also included in the console output, there is a line for the duration in number of seconds and the weather station names as part of the output during the ingestion of each file.

The lengthy time is due to using a full blown MySQL database inside a Docker container running on a very old MacBook.  I initially wrote some throw away code and ingested to a natively installed SQLite database on the very same MacBook.  It took only 10.72 seconds to completely ingest all 1729957 records into SQLite!  Since I tried this first, I was shocked that the same process took exponentially longer to ingest into a full fledged database.

For a full comparison, I saved console output to log files in `./answers/console_logs`.

## Problem 3 - Data Analysis

The data model for data analysis is also in the same documents mentioned in the answer to problem 1 above.  I named the table `WeatherWatcher.weather_statistics`.  The code to populate this table is `./weather_watcher/compute.py`.

## Problem 4 - REST API

I chose FastAPI as my REST API Web Framework because I am very familiar with it, which made it faster for me to write the API code for it.  It also includes a Swagger / OpenAPI endpoint for automated documentation of my API.  I created 3 REST API endpoints:

1. `/api/weather` - produces paginated json results of the ingested data stored inside the weather_measurements table.  Allows for optionally filtering by date and/or by station_id.  Default paging parameters are offset=0 and limit=20.
2. `/api/weather/stats` - produces paginated json results of the computed data analysis statistics data stored inside the weather_statistics table.  Allows for optionally filtering by year and/or by station_id.  Default paging parameters are offset=0 and limit=20.
3. `/api/weather/stations` - produces paginated json results of the ingested data stored inside the weather_stations table.  Allows for optionally filtering by date and/or by station_id.  Default paging parameters are offset=0 and limit=20.

I saved the API output from visiting the endpoints in a browser to `./answers/api_output/`.  I included PDF printouts from the browser as well as the json formatted results.

I saved the Swagger / OpenAPI output covering all the permutations of expanding sections and running trial executions to this location: `./answers/openapi_docs/`.

I created unit tests in `./weather_watcher_tests/api_test.py` that verifies these 5 assertions for each of the 3 REST API endpoints:

1. Response HTTP status code comes back as 200 OK.
2. The length of the response json matches the default limit of 20 records.
3. The response json is a list.
4. The first item in the list is a dict.
5. The fields or keys in the first item match the expected fields from the DDL statement.

Output from running the unit test is stoed in `./answers/console_logs/output_unit_tests.log`

## Extra Credit - Deployment

To get this code running in the AWS cloud, I would start with a Docker image that has a shell environment like my development environment.  I would create a Dockerfile to customize such an image so that it has the correct Python, pip, and their required dependencies installed to run FastAPI.  I could then push this image up to AWS ECR.  Then I could use ECS Fargate clusters to pull and run the image from the AWS repo.  I can configure API Gateway to allow for public access to the endpoints in my ECS instances.

For the database, I would use RDS to setup MySQL Server.  Using RDS, I could enjoy all the benefits that it comes with, including its performance, scalability, high availability, security, and ease of operations like upgrading, provisioning and backups.

## Submitting Your Answers

Main technologies used for this project include:

1. Hardware: MacBook
2. OS: macOS Mojave v10.14.6
3. Shell: /bin/bash
4. Primary Languauge: Python v3.12.4
5. IDE: VSCode
6. Linter: Flake8
7. Code Formatter: Black
8. Testing: Pytest
9. Container SW: Docker / Docker Desktop
10. Database: MySQL Server v5.7.20
11. REST API Web Framework: FastAPI

As noted above, I used Flake8 as my linter and Black as my code formatter.  I installed the plugins for them inside my IDE for automated problem detection and quick fixes.  I named many functions and variables in such a way that makes the code self-documenting, but also embedded code comments to help with parts where it may require more explanation for reviewers to understand.  A link to this forked repo will be provided from me to the requestor via email.

<br />
<br />
<br />

# HOW TO RUN - TLDR Version

### 1. Setup Environment Variables
Create a .env file at the root folder of your locally cloned copy of this repo to store all the necessary environment variables.  You may enter your own password and/or update the IP addresses and port as needed.

```
MYSQL_SERVER=127.0.0.1
MYSQL_ROOT_HOST=172.17.0.1
MYSQL_DATABASE=WeatherWatcher
MYSQL_USER=root
MYSQL_PASSWORD=IamR00T!!!
MYSQL_PORT=3306
```

### 2. Run Commands
Below is the ordered list of commands needed to run everything from the root folder of your local clone in this exercise.  A bash shell environment or something very similar is required to run these commands.  Python, pip, and Docker must be installed in the shell environment.  Other dependencies should be resolved by installing the required Python packages using the pip command that is listed.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export $(cat .env)
chmod +x run_mysql_docker.sh
./run_mysql_docker.sh
alembic upgrade head
python -m weather_watcher.ingest
python -m weather_watcher.compute
pytest weather_watcher_tests/api_test.py -s
python -m uvicorn weather_watcher.main:app --reload  
```

### 3. Visit URLs

These are the URLs used for this exercise once the above commands have run successfully:

1. http://127.0.0.1:8000/api/weather/ - JSON list of the first 20 records that were ingested into the WeatherWatcher.weather_measurements database table.
2. http://127.0.0.1:8000/api/weather/stats - JSON list of the fisrt 20 records that were computed for the Data Analysis portion of this exercise, pulling data from the WeatherWatcher.weather_statistics database table.
3. http://127.0.0.1:8000/api/weather/stations - JSON list of the first 20 records that were ingested into the WeatherWatcher.weather_stations database table.  Although not required, but it was easy to do and allows for manual, quick sanity checks.
4. http://127.0.0.1:8000/docs - Swagger/OpenAPI automated self-documentation of the REST API represented by the previous 3 URLs in this list, complete with the usual "Try it out" feature.

PDF printouts of my sample runs are provided in the ``./answers`` section.

<br />
<br />
<br />

# HOW TO RUN - Verbose Version

Assuming you've read through the CliffsNotes version of How to Run the code, in this section, I will provide a bit more detail about each command that was listed in the Run Commands section above.  Using the same order, I will group the commands into logical sections in my explanation below.

## 1. Setup Environment
The first two lines are for creating your virtual environment and then activating it, respectively.  The third line is to install all of the required Python dependencies using pip along with the provided requirements.txt file.
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Setup Database
With the .env file created, the first command exports the required environment variables and their values into your shell environment.  Next, chmod sets the permission of the script so that it can be executed.  The third command executes the shell script to create and run the Docker container using the MySQL v5.7.20 image.  The database catalog "WeatherWatcher" gets created with this step as well.  The alembic command then runs the Python migration scripts to create the 3 tables used in this exercise.
```
export $(cat .env)
chmod +x run_mysql_docker.sh
./run_mysql_docker.sh
alembic upgrade head
```

## 3. Ingest Files and Perform Data Analysis
The first line below uses the Pandas libary to ingest the raw files of data into the database.  The compute command will run the data analysis and store its statistics into a separate table.
```
python -m weather_watcher.ingest
python -m weather_watcher.compute
```

Alternatively, if you are not fond of spotted bears, you may run this command to ingest the data without using the Pandas library.
```
python -m weather_watcher.ingest_without_pandas
```

## 4. Run Unit Tests
This runs the unit tests against my REST API code.  It tests the 3 endpoints with 5 assertions as described in the Answers section of this README document.
```
pytest weather_watcher_tests/api_test.py -s 
```

## 5. Run FastAPI Web Server
This runs the FastAPI Web Server in the console, thereby allowing the 3 endpoints and the swagger docs to be visited.
```
python -m uvicorn weather_watcher.main:app --reload  
```

If an error appears stating that the "Address already in use", it could be that you have another server running.  To kill it off, you can run the command below before attempting to run the above command again.
```
sudo lsof -t -i tcp:8000 | xargs kill -9
```