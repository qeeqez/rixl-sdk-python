#!/usr/bin/env bash
# Regenerate the Python SDK from the upstream RIXL OpenAPI spec.
set -euo pipefail

kiota generate \
    -l python \
    -c RixlClient \
    -n rixl_sdk \
    -d https://raw.githubusercontent.com/rixlhq/openapi/refs/heads/main/openapi.yaml \
    -o "$(dirname "$0")/sdk" \
    --clean-output \
    --exclude-backward-compatible
