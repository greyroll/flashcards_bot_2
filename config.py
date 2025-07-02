import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

relative_db_path = os.getenv("DB_PATH")
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = (BASE_DIR / relative_db_path).resolve()