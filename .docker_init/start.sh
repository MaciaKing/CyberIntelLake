#!/bin/bash
# .docker_init/start.sh
set -e

echo "MACIAAAA"

ROOT_DIR="/app"
cd $ROOT_DIR
export PYTHONPATH=$ROOT_DIR:$PYTHONPATH

# Inicializar la base de datos
python -m database.init_db

tail -f /dev/null
