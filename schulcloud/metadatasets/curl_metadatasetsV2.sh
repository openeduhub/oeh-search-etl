#!/bin/bash

# Through the web interface. [Not working!]
# message_to_detect='edu-sharing Docker Demo'
# until [ "`curl --silent --show-error --connect-timeout 1 http://localhost:80 | grep \"$message_to_detect\"`" != "" ];

# Through the tomcat log files. [Works!]
message_to_detect='INFO: Server startup in '
until [ "`cat /usr/local/tomcat/logs/catalina* | grep \"$message_to_detect\"`" != "" ];
do
  echo --- sleeping for 10 seconds
  sleep 10
done

echo Tomcat is ready!

curl    -X PUT \
        --header 'Content-Type: application/json' \
        --user admin:admin \
        --header 'Accept: application/xml' \
        -d '{"metadatasetsV2":"mds,mds_oeh"}' \
        'http://127.0.0.1/edu-sharing/rest/admin/v1/applications/homeApplication.properties.xml'