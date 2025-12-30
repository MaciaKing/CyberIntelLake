#!/bin/bash
set -e

ROOT_DIR="/app"
cd $ROOT_DIR
export PYTHONPATH=$ROOT_DIR:$PYTHONPATH

# Wait for db connection
.docker_init/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -t 30 -- echo "PostgreSQL service ready"

# Init db
python3 -m database.init_db

python3 -m schedule.scheduler

tail -f /dev/null
