#!/bin/bash

echo "Which environment?"
ls -a |grep "\\.env\\." |sed "s/\\.env.//g"
read env

source ../../../.venv/bin/activate

set -a  # enable bash variables to be exported to environment
source .env
source ".env.$env"
set +a
