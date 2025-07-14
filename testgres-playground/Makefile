build:
	podman build -t localhost/glvd-testgres:latest .

run:
	podman run -it --rm --name=glvd-testgres --publish 5432:5432 --env POSTGRES_USER=glvd --env POSTGRES_DB=glvd --env POSTGRES_PASSWORD=glvd localhost/glvd-testgres:latest postgres -c log_statement=all
