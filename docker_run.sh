#!/bin/bash

crawler="hello_world"
schedule="*-*-12:45"
blacklist="/oeh-search-etl/schulcloud/sodix/blacklist.json"
docker run -it -e "EDU_SHARING_BASE_URL=$EDU_SHARING_BASE_URL" -e "EDU_SHARING_USERNAME=$EDU_SHARING_USERNAME" -e "EDU_SHARING_PASSWORD=$EDU_SHARING_PASSWORD" -e "SODIX_USER=$SODIX_USER" -e "SODIX_PASSWORD=$SODIX_PASSWORD" -e "SODIX_BLACKLIST_PATH=$blacklist" -e "SCHEDULE=$schedule" -e "CRAWLER=$crawler" oeh-search-etl
