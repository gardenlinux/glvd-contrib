FROM ghcr.io/gardenlinux/glvd-postgres:edgenotls

COPY glvd.sql /docker-entrypoint-initdb.d/glvd.sql
