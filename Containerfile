FROM ghcr.io/gardenlinux/glvd-postgres:edge

COPY glvd.sql /docker-entrypoint-initdb.d/glvd.sql
