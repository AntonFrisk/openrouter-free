"""Persist the ranked free-model list inside this project only."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import yaml


def project_root() -> Path:
    """Directory of this package's pyproject.toml."""
    for p in Path(__file__).resolve().parents:
        py = p / "pyproject.toml"
        if py.is_file() and 'name = "orfree"' in py.read_text(encoding="utf-8"):
            return p
    return Path(__file__).resolve().parent


PROJECT_ROOT = project_root()
STATE_PATH = PROJECT_ROOT / "models.yml"
ENV_PATH = PROJECT_ROOT / ".env"


def load(path: Path = STATE_PATH) -> dict:
    if not path.exists():
        return {"fetched_at": None, "models": []}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {"fetched_at": data.get("fetched_at"), "models": list(data.get("models") or [])}


def save(state: dict, path: Path = STATE_PATH) -> None:
    path.write_text(
        yaml.safe_dump(
            {"fetched_at": state.get("fetched_at"), "models": state.get("models") or []},
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def is_stale(state: dict, refresh_hours: float) -> bool:
    raw = state.get("fetched_at")
    if not raw or not state.get("models"):
        return True
    fetched = datetime.fromisoformat(str(raw))
    if fetched.tzinfo is None:
        fetched = fetched.replace(tzinfo=timezone.utc)
    age = datetime.now(timezone.utc) - fetched
    return age.total_seconds() > refresh_hours * 3600


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
