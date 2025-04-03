FROM ghcr.io/gardenlinux/glvd-postgres:latest

COPY schema-a.sql /docker-entrypoint-initdb.d/schema.sql

