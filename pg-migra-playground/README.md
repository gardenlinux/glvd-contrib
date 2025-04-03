
This is a playground for diffing postgres schemas in order to create migrations using [migra](https://github.com/djrobstep/migra)

```
podman exec -it pg-migra-playground-migra-1 bash -c "migra postgresql://glvd:glvd@db-a:5432/glvd?sslmode=disable postgresql://glvd:glvd@db-b:5432/glvd?sslmode=disable"
```
