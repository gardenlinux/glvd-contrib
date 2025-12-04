build:
	podman build -t localhost/glvd-postgres-img-based:latest .

run:
	podman run -it --rm --name=glvd-postgres-img --publish 5432:5432 --env POSTGRES_USER=glvd --env POSTGRES_DB=glvd --env POSTGRES_PASSWORD=glvd localhost/glvd-postgres-img-based:latest postgres -c log_statement=all
