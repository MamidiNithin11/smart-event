#!/bin/bash
set -e

echo "=== Vercel Build: Running database migrations ==="

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Run Alembic migrations against the production database
echo "Running Alembic migrations..."
uv run --project server alembic -c server/alembic.ini upgrade head

echo "=== Migrations complete ==="

# Continue with the standard Vercel build
echo "=== Continuing with npm build ==="
