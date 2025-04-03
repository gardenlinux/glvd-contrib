FROM ghcr.io/gardenlinux/glvd-postgres:latest

COPY schema-b.sql /docker-entrypoint-initdb.d/schema.sql

