 FROM edusharing/repo-rs-moodle:sc-latest
# Tested on FROM edusharing/repo-rs-moodle:sc-2a81f4d31
#
# Production version, on mv-repo, (0f18b0ce2) not available in Docker Hub:
# https://hub.docker.com/r/edusharing/repo-rs-moodle/tags

# Copy the metadatasets file to the container, while changing the permissions to the correct user:group.
COPY --chown=tomcat:tomcat \
       metadatasets/mds_oeh_17_09_2020.xml \
       /usr/local/tomcat/shared/classes/org/edu_sharing/metadataset/v2/xml/mds_oeh.xml

# Add the script that will wait and add the mds_oeh_24_06_2020.xml at the right time.
ADD metadatasets/curl_metadatasetsV2.sh /root/curl_metadatasetsV2.sh

# sleep infinity as otherwise immediately after the container would start the container would exit.
CMD /root/curl_metadatasetsV2.sh; sleep infinity
