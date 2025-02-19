#!/bin/bash

# Available commands/options:
#
# ./docker.sh shell
#     - opens a new shell for the running container
#
# ./docker.sh stop
#     - stop all running a docker containers
#     - does not stop the postgres container
#
# ./docker.sh clean
#     - stop all running a docker containers and remove them
#     - does not stop the postgres container
#
# ./docker.sh
#     - run the application

DOCKER_NAME=log-monitoring-container

if [[ ${1} == "clean" ]]; then
  docker stop $(docker ps -a --filter name=${DOCKER_NAME} -q)
  docker rm $(docker ps --filter name=${DOCKER_NAME} -q --filter status=exited)
elif [[ ${1} == "stop" ]]; then
  docker stop $(docker ps -a --filter name=${DOCKER_NAME} -q)
elif [[ ${1} == "shell" ]]; then
  docker exec -it $(docker ps --filter name=${DOCKER_NAME} -q) \
    bash -c 'cd /app && python -m venv venv && source venv/bin/activate venv && /bin/bash'
else
  docker rm $(docker ps --filter name=${DOCKER_NAME} -q --filter status=exited)
  docker-compose run --service-ports --name ${DOCKER_NAME} app bash
fi
