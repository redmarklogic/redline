# Version Guard Report — Skipped

No dependency sources found (no lockfile, package.json, or tech stack decision record).

Note (feature 111): this is an infrastructure feature (DNS + Firebase Hosting proxy +
Cloud Run). The relevant tool versions are outside version-guard's npm scope and are
pinned instead in the plan's Technical Context: firebase-tools (current major verified
against official docs in the DevOps research, 2026-06-11), gcloud CLI, Terraform
google/cloudflare providers (ADR-020). Cloudflare API is version-pinned by URL (v4).
