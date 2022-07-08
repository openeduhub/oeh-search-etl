#!/bin/bash

echo Pulling repository...
git pull

source ../../../.venv/bin/activate
source load_env.sh

echo "To which environment do you want to apply the permissions?"
ls -a |grep "\\.env\\." |sed "s/\\.env.//g"
echo
read env

set -a
source ".env.$env"
set +a

python permissions.py
