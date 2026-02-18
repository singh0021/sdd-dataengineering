#!/bin/bash
# -- ----------------------------------
# -- FSI Lakehouse Deployment Script
# -- Usage: ./scripts/deploy.sh [dev|staging|prod]
# -- ----------------------------------

set -e

TARGET=${1:-dev}
VALID_TARGETS=("dev" "staging" "prod")

# Validate target
if [[ ! " ${VALID_TARGETS[@]} " =~ " ${TARGET} " ]]; then
    echo "Error: Invalid target '$TARGET'. Must be one of: ${VALID_TARGETS[*]}"
    exit 1
fi

echo "========================================"
echo "FSI Lakehouse Deployment"
echo "Target: $TARGET"
echo "========================================"

# Validate bundle
echo "[1/4] Validating bundle configuration..."
databricks bundle validate -t "$TARGET"

# Deploy bundle
echo "[2/4] Deploying bundle to $TARGET..."
databricks bundle deploy -t "$TARGET"

# Sync files
echo "[3/4] Syncing pipeline files..."
databricks bundle sync -t "$TARGET"

echo "[4/4] Deployment complete!"
echo ""
echo "To run the pipeline:"
echo "  databricks bundle run fsi_fraud_detection_pipeline -t $TARGET"
echo ""
echo "To view pipeline status:"
echo "  databricks pipelines list"
