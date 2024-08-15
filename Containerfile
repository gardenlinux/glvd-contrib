FROM ghcr.io/gardenlinux/glvd-postgres:edgenotls

COPY schema.sql /docker-entrypoint-initdb.d/schema.sql
