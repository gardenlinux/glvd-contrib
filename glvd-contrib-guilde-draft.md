# Contributing to GLVD

State:
This document is a DRAFT.

## Project Overview

The code of glvd is located in multiple repositories inside the `gardenlinux` org on GitHub.

glvd is implemented in various components.

### [gardenlinux/glvd](https://github.com/gardenlinux/glvd)

The `gardenlinux/glvd` repo is the main entry point to GLVD.
It contains project-wide docs, and infrastructure definitions for deploying GLVD instances both locally and in cloud environments.

### [`gardenlinux/glvd-postgres`](https://github.com/gardenlinux/glvd-postgres)

A postgres database is the central component of glvd.
This repository contains a Containerfile to run this database.

### [`gardenlinux/glvd-data-ingestion`](https://github.com/gardenlinux/glvd-data-ingestion)

Data ingestion creates the required database schema and imports data from external sources such as NVD and the debian security tracker.

### [`https://github.com/gardenlinux/glvd-api`](https://github.com/gardenlinux/glvd-api)

The backend api exposed an HTTP API to get data out of the database.

It also contains a simple web interface.

### [`https://github.com/gardenlinux/package-glvd`](https://github.com/gardenlinux/package-glvd)

The cli client is available in the Garden Linux APT repo.

## Setup a Local Dev Env

### On macOS, using podman (desktop/machine)

- Make sure [podman is setup properly](https://podman.io/docs/installation)
- Get the suitable [docker compose](https://github.com/docker/compose) binary and put it into your `PATH`
  - Running `podman compose` will use a 'provider' for working with compose files
  - By default, it makes use of https://github.com/containers/podman-compose, which does not support all features neede by GLVD as of december 2024
  - If the `docker-compose` binary is in your `PATH`, `podman compose` will use that to crate containers
  - Using this method, you can use podman to run GLVD

With this setup, inside your local clone of the `gardenlinux/glvd` repo, you should be able to run `podman compose --file deployment/compose/compose.yaml up` which will bring up a local glvd environment including a recent snapshot of the database.

You can check this using the Spring Boot Actuator endpoint:

```
$ curl http://localhost:8080/actuator/health
{"status":"UP"}
```

Congratulations, you have a running instance of GLVD.

Let's have a closer look at our running containers:

```
$ podman ps
CONTAINER ID  IMAGE                                            COMMAND               CREATED      STATUS                  PORTS                   NAMES
aaaaaaaaaaaa  ghcr.io/gardenlinux/glvd-postgres:latest         postgres              2 weeks ago  Up 3 minutes (healthy)  0.0.0.0:5432->5432/tcp  compose-glvd-postgres-1
bbbbbbbbbbbb  ghcr.io/gardenlinux/glvd-api:latest              /jre/bin/java -ja...  2 weeks ago  Up 3 minutes            0.0.0.0:8080->8080/tcp  compose-glvd-1
```

We have two long-running containers:
The postgres db, and our backend.

The db exposes the default port `5432`, which is useful for development purposes.
You may use postgres client applications to inspect, edit, backup or restore the database as needed.
In a production deployment, the database is not exposed to the outside world.

The backend exposed port 8080 as we have already seen above in our `curl` command.

### Exploring the API

Next, make yourself familiar with GLVD's HTTP API.
It is documented [here](https://gardenlinux.github.io/glvd-api/).

> [!TIP]
> For using your local instance, you'll need to use `http://localhost:8080` in all of the api urls instead of the provided urls.

After getting familiar with the API, you can have a look at the [example requests provided in the glvd-api repo](https://github.com/gardenlinux/glvd-api/tree/main/api-examples).

### Make changes to the backend and try them out

Prerequisites:
- JDK 21 (SapMachine preferred, download and install from https://sapmachine.io)
  - Be sure to install the *JDK* version, the *JRE* is not enough

Run `./gradlew bootJar` inside the `glvd-api` repo checkout to compile the backend.

Run `podman stop compose-glvd-1` to stop the backend container from running.
This allows your locally built backend to make use of the port 8080 on your machine.

Run `java -jar build/libs/glvd-0.0.1-SNAPSHOT.jar` to start the backend version you've just built.
It should start up and connect to the database automatically.

Run `curl http://localhost:8080/actuator/health` again and observe the log of your backend instance.
It should say something like `Initializing Servlet 'dispatcherServlet'`.

Congratulations, you compiled the GLVD backend on your own, and are running it on your machine.
You can now make changes to the source code, stop, rebuild and restart your instance and see if it does what you expect.

### Run automated tests locally

todo: this setup is not ideal, testcontainers and podman are not friends, needs rework

