FROM ghcr.io/gardenlinux/glvd-postgres:edgenontls

COPY glvd.sql /docker-entrypoint-initdb.d/glvd.sql
