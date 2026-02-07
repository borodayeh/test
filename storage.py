import json
import os
from datetime import datetime

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "work_minutes": 60,
    "break_minutes": 5,
    "completed_breaks": 0,
    "last_run": "",
    "autostart_enabled": False,
}


def load_data(file_path: str = DATA_FILE) -> dict:
    """Load app data from JSON or create defaults."""
    if not os.path.exists(file_path):
        data = DEFAULT_DATA.copy()
        data["last_run"] = datetime.now().isoformat(timespec="seconds")
        save_data(data, file_path)
        return data

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        data = DEFAULT_DATA.copy()

    for key, value in DEFAULT_DATA.items():
        data.setdefault(key, value)

    data["last_run"] = datetime.now().isoformat(timespec="seconds")
    save_data(data, file_path)
    return data


def save_data(data: dict, file_path: str = DATA_FILE) -> None:
    """Save app data to JSON file."""
    print(f"[LOG] Saving data into {file_path}")
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
