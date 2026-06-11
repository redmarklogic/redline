# deploy/

Deployment artefacts for all services in the monorepo.

## Layout

```
deploy/
  docker/
    <service-name>/
      Dockerfile        # multi-stage image for that service
      .env.example      # documents required and optional env vars
  infra/
    bootstrap/          # one-off GCP project + state bucket creation
    terraform/          # all GCP infrastructure as HCL
```

## Adding a second service

1. Create `deploy/docker/<service-name>/Dockerfile`.
2. Add a service entry to `docker-compose.yml` at the repo root:
   ```yaml
   services:
     <service-name>:
       build:
         context: .
         dockerfile: deploy/docker/<service-name>/Dockerfile
       platform: linux/amd64
       ports:
         - "${SERVICE_PORT:-<default>}:<container-port>"
   ```
3. Add `deploy/docker/<service-name>/.env.example` documenting the new service's env vars.

No changes to the `marker` service configuration are needed.

## Running the local stack

```powershell
# Start all services
docker compose up -d

# Check health
Invoke-WebRequest http://localhost:8000/health

# Tear down
docker compose down
```

## Building an image directly

```powershell
docker build --platform linux/amd64 -t marker:local -f deploy/docker/marker/Dockerfile .
```

## One-command local smoke check

Build, start, hit `/health`, then stop — all in one pipeline:

```powershell
docker build --platform linux/amd64 -t marker:smoke -f deploy/docker/marker/Dockerfile . `
  && docker run -d --name marker-smoke -e PORT=8080 -p 8080:8080 marker:smoke `
  && Start-Sleep 12 `
  && Invoke-WebRequest http://localhost:8080/health `
  && docker stop marker-smoke `
  && docker rm marker-smoke
```

The container listens on `PORT` (default 8080). In local compose, `MARKER_PORT` (default 8000)
maps the host side: `"${MARKER_PORT:-8000}:8080"` — so `localhost:8000/health` also works when
the stack is up via `docker compose up`.
