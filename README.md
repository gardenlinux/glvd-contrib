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

## Dev VM

In case you want to have a local setup for playing with GLVD, you might use this [lima vm](https://github.com/lima-vm/lima) setup:

```bash
# With lima installed, you can setup the environment like this
host$ limactl create --name=glvd-temp dev-vm.yaml
host$ limactl start glvd
host$ limactl shell glvd

# You may start the database as a container like so
glvd$ podman run -it --rm -p 5432:5432 -e POSTGRES_USER=glvd -e POSTGRES_PASSWORD=glvd -e POSTGRES_DB=glvd ghcr.io/gardenlinux/glvd-postgres:edge

# You have access to the glvd commands
glvd$ which glvd
/home/user.linux/.local/bin/glvd
glvd$ which glvd-data
/home/user.linux/.local/bin/glvd-data
```



## Setup glvd with local service

In _this_ directory, run:

```bash
glvd-contrib$ podman build -t my-glvd-postgres .
glvd-contrib$ podman run -it --rm -p 5432:5432 -e POSTGRES_USER=glvd -e POSTGRES_PASSWORD=glvd -e POSTGRES_DB=glvd  localhost/my-glvd-postgres:latest

```

In the _glvd_ directory, run:

```bash
glvd$ virtualenv myvirtualenv
glvd$ source myvirtualenv/bin/activate
venv-in-glvd$ pipx install poetry
venv-in-glvd$ poetry install
venv-in-glvd$ export PGUSER=glvd
venv-in-glvd$ xport PGDATABASE=glvd
venv-in-glvd$ export PGPASSWORD=glvd
venv-in-glvd$ export PGHOST=localhost
venv-in-glvd$ export PGPORT=5432
venv-in-glvd$ PYTHONPATH=src quart --app glvd.web run
```

It's now expected that you can interact with the HTTP API on your host, for example:

```bash
$ curl http://127.0.0.1:5000/readiness
{"db_check":{"status":"ok"},"status":"ok"}
```
