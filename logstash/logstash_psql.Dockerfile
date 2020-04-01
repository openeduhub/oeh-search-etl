FROM docker.elastic.co/logstash/logstash:7.4.2

RUN rm -f /usr/share/logstash/pipeline/logstash.conf

COPY pipeline/ /usr/share/logstash/pipeline/
COPY templates/ /usr/share/logstash/templates/

COPY --chown=logstash:root postgresql-42.2.12.jar /usr/share/logstash/logstash-core/lib/jars/postgresql-42.2.12.jar

RUN logstash-plugin install logstash-input-jdbc