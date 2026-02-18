#!/bin/bash
# -- ----------------------------------
# -- Destroy FSI Lakehouse Deployment
# -- Usage: ./scripts/destroy.sh [dev|staging|prod]
# -- ----------------------------------

set -e

TARGET=${1:-dev}

echo "========================================"
echo "WARNING: Destroying FSI Lakehouse"
echo "Target: $TARGET"
echo "========================================"

read -p "Are you sure you want to destroy the deployment? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo "Destroying bundle..."
databricks bundle destroy -t "$TARGET" --auto-approve

echo "Deployment destroyed successfully."
