#!/bin/bash
# -- ----------------------------------
# -- Run FSI Lakehouse Pipeline
# -- Usage: ./scripts/run_pipeline.sh [dev|staging|prod] [--full-refresh]
# -- ----------------------------------

set -e

TARGET=${1:-dev}
FULL_REFRESH=${2:-""}

echo "========================================"
echo "Running FSI Fraud Detection Pipeline"
echo "Target: $TARGET"
echo "Full Refresh: ${FULL_REFRESH:-false}"
echo "========================================"

if [ "$FULL_REFRESH" == "--full-refresh" ]; then
    echo "Starting full refresh..."
    databricks bundle run fsi_fraud_detection_pipeline -t "$TARGET" --full-refresh
else
    echo "Starting incremental update..."
    databricks bundle run fsi_fraud_detection_pipeline -t "$TARGET"
fi

echo ""
echo "Pipeline triggered successfully!"
