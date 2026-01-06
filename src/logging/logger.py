import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "interactions.jsonl"

def log_interaction(record: Dict[str, Any]) -> None:
    enriched = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        **record,
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(enriched) + "\n")
