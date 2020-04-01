FROM postgres:12.2

COPY data/layout.sql /docker-entrypoint-initdb.d