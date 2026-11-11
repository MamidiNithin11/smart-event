from pathlib import Path
import sys

SERVER_DIRECTORY = Path(__file__).resolve().parents[1] / 'server'
sys.path.insert(0, str(SERVER_DIRECTORY))

from app.main import app
