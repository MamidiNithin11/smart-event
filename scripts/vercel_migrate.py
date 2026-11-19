#!/usr/bin/env python3
"""
Run Alembic migrations for Vercel deployment.
This script is called by the Vercel build process to ensure the database
schema is up to date before the application starts serving requests.
"""
import sys
from pathlib import Path

# Add the server directory to the Python path
SERVER_DIR = Path(__file__).resolve().parents[1] / "server"
sys.path.insert(0, str(SERVER_DIR))

from alembic.config import Config
from alembic import command

def main():
    print("=== Running Alembic Migrations ===")

    alembic_cfg = Config(SERVER_DIR / "alembic.ini")

    try:
        command.upgrade(alembic_cfg, "head")
        print("=== Migrations completed successfully ===")
    except Exception as e:
        print(f"ERROR: Migration failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
