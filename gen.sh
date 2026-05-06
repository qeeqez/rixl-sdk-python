#!/usr/bin/env bash
# Regenerate the Python SDK from the upstream RIXL OpenAPI spec.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SDK_DIR="${SCRIPT_DIR}/sdk"

rm -rf "${SDK_DIR}"
mkdir -p "${SDK_DIR}"

kiota generate \
    -l python \
    -c RixlClient \
    -n rixl_sdk \
    -d https://raw.githubusercontent.com/rixlhq/openapi/refs/heads/main/openapi.yaml \
    -o "${SDK_DIR}" \
    --clean-output \
    --exclude-backward-compatible
