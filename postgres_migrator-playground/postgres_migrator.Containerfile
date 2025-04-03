FROM rust:latest AS builder
WORKDIR /usr/src/

RUN cargo install postgres_migrator


FROM python:3
RUN pip install migra~=3.0.0 psycopg2-binary~=2.9.3 setuptools

WORKDIR /foo

RUN mkdir schema migrations

COPY --from=builder /usr/local/cargo/bin/postgres_migrator /usr/bin/

COPY schema-b.sql schema/schema.sql
