from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
SRC_PATH = ROOT_DIR / "alert_volume" / "src"

LOGS_PATH = ROOT_DIR / "" / "data" / "logs"
DATA_PATH = SRC_PATH / "data"
USER_DATA_PATH = ROOT_DIR / "alert_volume" / "data"
DB_PATH = USER_DATA_PATH / "coin_stats.db"

ASYNC_DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"
SYNC_DB_URL = f"sqlite:///{DB_PATH}"
