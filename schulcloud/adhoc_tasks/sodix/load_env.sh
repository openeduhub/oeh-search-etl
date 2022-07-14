
#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 ENV"
  echo "ENV should correspond to an environment file in converter/"
  exit 0
fi

if [ `basename $(pwd)` != "sodix" ]; then
  echo "This script should be called from oeh-search-etl/schulcloud/adhoc_tasks/sodix"
  exit 1
fi

environment=$1

env_file=".env.$1"

if [ ! -f "$env_file" ]; then
  echo "Environment file $env_file does not exist"
  exit 1
fi

echo Pulling repository...
git pull

set +a
source $env_file
set -a

source ../../../.venv/bin/activate
