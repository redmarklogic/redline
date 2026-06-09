# deploy/modules/

Infrastructure scripts and helpers for CI pipelines, container startup, and cloud provisioning.

## Naming convention

Files are named by concern: `<concern>-<verb>.sh` or `<concern>-<verb>.ps1`.

Examples:
- `startup-wait.sh` — polls a service until healthy before proceeding
- `migrate-db.sh` — runs database migrations on container start

## What belongs here

- Startup/init scripts executed by containers or CI jobs
- CI helper scripts (scan, lint, publish) that are too tightly coupled to this repo to live elsewhere
- One-off provisioning scripts that are not Terraform/Pulumi modules

## What does NOT belong here

- Terraform modules or cloud-provider infra-as-code (use a dedicated `infra/` tree)
- Application source code
- Per-service Dockerfiles (those live at `deploy/docker/<service>/Dockerfile`)
