#!/bin/bash

crawler="$1"
schedule="now"
docker run -it --network="host" -e "SPLASH_URL=$SPLASH_URL" -e "EDU_SHARING_BASE_URL=$EDU_SHARING_BASE_URL" -e "EDU_SHARING_USERNAME=$EDU_SHARING_USERNAME" -e "EDU_SHARING_PASSWORD=$EDU_SHARING_PASSWORD" -e "SODIX_USER=$SODIX_USER" -e "SODIX_PASSWORD=$SODIX_PASSWORD" -e "S3_ACCESS_KEY=$S3_ACCESS_KEY" -e "S3_SECRET_KEY=$S3_SECRET_KEY" -e "S3_ENDPOINT_URL=$S3_ENDPOINT_URL" -e "S3_BUCKET_NAME=$S3_BUCKET_NAME" -e "S3_REGION=$S3_REGION" -e "S3_DOWNLOAD_DIRECTORY=$S3_DOWNLOAD_DIRECTORY" -e "SCHEDULE=$schedule" -e "CRAWLER=$crawler" oeh-search-etl
