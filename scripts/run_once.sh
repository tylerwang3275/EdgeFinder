#!/usr/bin/env bash
set -euo pipefail

# EdgeFinder run script for cron/CI
# Usage: ./scripts/run_once.sh

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Change to project directory
cd "$(dirname "$0")/.."

# Run the pipeline
python -m src.main run

echo "EdgeFinder pipeline completed successfully"
