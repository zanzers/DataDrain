import json
import os
from datetime import datetime

APP_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "DataDrain")
os.makedirs(APP_DIR, exist_ok=True)
SAVE_FILE = os.path.join(APP_DIR, "datadrain.json")


def save_state(remaining: int) -> None:
    data = {
        "remaining": remaining,
        "updated": datetime.now().isoformat(timespec="seconds"),
    }
    tmp = SAVE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.replace(tmp, SAVE_FILE)   # atomic: never leaves a half-written file


def load_state():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None