#!/bin/bash
export $(cat .env)
docker run -d \
  --name mysql-docker-container \
  -e MYSQL_ROOT_HOST=$MYSQL_ROOT_HOST \
  -e MYSQL_DATABASE=$MYSQL_DATABASE \
  -e MYSQL_ROOT_PASSWORD=$MYSQL_PASSWORD \
  -p $MYSQL_PORT:$MYSQL_PORT \
  mysql/mysql-server:5.7.20
