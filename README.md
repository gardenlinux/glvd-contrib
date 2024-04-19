# glvd-contrib
Scripts related to GLVD. Used as a staging area for things that might be useful.


## Create a SQL database dump

Run the GitHub Workflow `.github/workflows/ingest-snapshot.yaml`

One the job is done you can download `glvd.sql`.

## Load the database dump locally

Place `glvd.sql` in this directory.
The file is huge, so it is on the gitignore list.

Build a container image from `Containerfile`.

```bash
podman build -t my-glvd-postgres .
```

Run the container:

```bash
podman run -it --rm -p 5432:5432 -e POSTGRES_USER=glvd -e POSTGRES_PASSWORD=glvd -e POSTGRES_DB=glvd  localhost/my-glvd-postgres:latest
```

You can now connect any local SQL client to localhost on the provided port/credentials.
