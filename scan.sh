#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# RedMark SonarQube -- branch scan (Bash)
# ---------------------------------------------------------------------------
# Bash parity of scan.ps1. Analyses the current redline branch against the
# local SonarQube instance (http://localhost:9000). Runs directly -- no CI.
# Usage:  ./scan.sh
# ---------------------------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

SCANNER_IMAGE='sonarsource/sonar-scanner-cli:11'
USETHIS_VERSION='usethis@0.22.0'

# -- 1. Load .env -----------------------------------------------------------
if [[ ! -f .env ]]; then
  echo "ERROR: .env not found. Copy .env.example to .env and set SONAR_TOKEN" >&2
  echo "       (generate one at http://localhost:9000 -> My Account -> Security)." >&2
  exit 1
fi
set -a
# shellcheck disable=SC1091
source .env
set +a

SONAR_HOST_URL="${SONAR_HOST_URL:-http://host.docker.internal:9000}"
SONAR_PROJECT_KEY="${SONAR_PROJECT_KEY:-redline}"
if [[ -z "${SONAR_TOKEN:-}" ]]; then
  echo "ERROR: SONAR_TOKEN is empty in .env. Generate a token at http://localhost:9000" >&2
  echo "       (My Account -> Security -> Generate Tokens) and set SONAR_TOKEN in .env." >&2
  exit 1
fi

# -- Availability check: single source of truth (sonar_scan.ensure_available) --
# Delegates to the Python tool so the scan and review gates share one definition
# of "available". SONARQUBE_URL is exported from .env above; the tool normalises
# host.docker.internal -> localhost for this host-side call.
export PYTHONPATH="$SCRIPT_DIR/.agents/tools"
if ! uv run python -m sonar_scan.healthcheck; then
  echo "ERROR: SonarQube availability check failed (see message above)." >&2
  exit 1
fi

# -- 2. Current branch ------------------------------------------------------
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[[ -n "$BRANCH" ]] || { echo "ERROR: could not determine git branch." >&2; exit 1; }
echo "-- Scanning branch: $BRANCH --"

# -- 3. Generate properties from the SSOT -----------------------------------
echo "-- Generating .cache/sonarqube/sonar-project.properties from [tool.usethis] --"
mkdir -p .cache/sonarqube
SONAR_PROJECT_KEY="$SONAR_PROJECT_KEY" uvx "$USETHIS_VERSION" show sonarqube --output-file=.cache/sonarqube/sonar-project.properties

# -- 4. Best-effort reports (absence must not fail the scan) -----------------
echo "-- Producing ruff report (best-effort) --"
uv run ruff check . --output-format=json -o .cache/sonarqube/ruff-report.json 2>/dev/null || true
[[ -f .cache/sonarqube/ruff-report.json ]] || echo '[]' > .cache/sonarqube/ruff-report.json

echo "-- Producing coverage report if data exists (best-effort) --"
if [[ -f .coverage ]]; then
  uv run coverage xml -o .cache/sonarqube/coverage.xml 2>/dev/null || echo "  coverage xml failed -- continuing."
else
  echo "  No .coverage data found -- skipping coverage."
fi

# -- 5. Run the scanner container against the local instance ----------------
TEMP_LOG=$(mktemp)
echo "-- Running $SCANNER_IMAGE --"
# Named volume persists the scanner cache (JRE/engine/plugins, ~150 MB) across
# the --rm containers; without it every scan re-downloads through the slow
# host.docker.internal loopback (measured 6m22s on a cold Docker Desktop).
# skipJreProvisioning uses the image's bundled JRE 17 instead of downloading one.
docker run --rm \
  -e "SONAR_HOST_URL=$SONAR_HOST_URL" \
  -e "SONAR_TOKEN=$SONAR_TOKEN" \
  -v "$SCRIPT_DIR:/usr/src" \
  -v "redmark-sonar-scanner-cache:/opt/sonar-scanner/.sonar" \
  "$SCANNER_IMAGE" \
  "-Dproject.settings=/usr/src/.cache/sonarqube/sonar-project.properties" \
  "-Dsonar.branch.name=$BRANCH" \
  "-Dsonar.scanner.skipJreProvisioning=true" | tee "$TEMP_LOG"
DOCKER_EXIT="${PIPESTATUS[0]}"
if [[ "$DOCKER_EXIT" -ne 0 ]]; then
  rm -f "$TEMP_LOG"
  echo "ERROR: sonar-scanner failed (exit $DOCKER_EXIT)." >&2; exit 1
fi

# -- 6. Poll compute-engine task (bounded wait, max 60 s) --------------------
CE_TASK_URL=$(grep -o 'http[s]*://[^ ]*api/ce/task[^ ]*' "$TEMP_LOG" | head -1 \
  | sed 's/host\.docker\.internal/localhost/')
rm -f "$TEMP_LOG"
[[ -n "$CE_TASK_URL" ]] || { echo "ERROR: Could not extract CE task URL from scanner output." >&2; exit 1; }

echo "-- Polling CE task (max 60 s): $CE_TASK_URL --"
CE_STATUS=''
for i in $(seq 1 12); do
  CE_STATUS=$(curl -fsS -H "Authorization: Bearer $SONAR_TOKEN" --max-time 10 "$CE_TASK_URL" \
    | sed -n 's/.*"status":"\([^"]*\)".*/\1/p')
  case "$CE_STATUS" in
    SUCCESS) break ;;
    FAILED|CANCELED) echo "ERROR: CE task $CE_STATUS: $CE_TASK_URL" >&2; exit 1 ;;
    *) echo "  status: $CE_STATUS - waiting 5 s..."; sleep 5 ;;
  esac
done
[[ "$CE_STATUS" == "SUCCESS" ]] \
  || { echo "ERROR: CE task did not finish within 60s: $CE_TASK_URL" >&2; exit 1; }
echo "  CE task: SUCCESS"

echo ""
echo "======================================================"
echo "  Scan complete for branch: $BRANCH"
echo "  Project: $SONAR_PROJECT_KEY"
echo "  View:    http://localhost:9000/dashboard?id=$SONAR_PROJECT_KEY&branch=$BRANCH"
echo "======================================================"
