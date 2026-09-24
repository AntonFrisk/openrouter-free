"""Route chat to the top free OpenRouter model, failing over on errors."""
from __future__ import annotations

import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from orfree.catalog import fetch_catalog, is_chat_like, merge
from orfree.rank import demote
from orfree.store import ENV_PATH, STATE_PATH, is_stale, load, now_iso, save

CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"


def _load_env() -> None:
    load_dotenv(ENV_PATH)


def _api_key() -> str:
    _load_env()
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("Missing OPENROUTER_API_KEY in .env")
    return key


def chat(model: str, prompt: str, timeout: int = 30) -> tuple[bool, float, str]:
    t0 = time.perf_counter()
    try:
        resp = requests.post(
            CHAT_URL,
            headers={"Authorization": f"Bearer {_api_key()}", "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role": "user", "content": prompt}]},
            timeout=timeout,
        )
        elapsed = time.perf_counter() - t0
        data = resp.json()
        if not resp.ok:
            return False, elapsed, data.get("error", {}).get("message") or resp.text[:120]
        content = (data["choices"][0]["message"].get("content") or "").strip()
        if not content:
            return False, elapsed, "empty content"
        return True, elapsed, content
    except requests.Timeout:
        return False, time.perf_counter() - t0, f"timed out after {timeout}s"
    except Exception as e:
        return False, time.perf_counter() - t0, str(e)


def ranked_models(refresh_hours: float = 24, timeout: int = 30, path: Path = STATE_PATH) -> list[str]:
    state = load(path)
    if is_stale(state, refresh_hours):
        try:
            catalog = fetch_catalog(_api_key(), timeout=timeout)
            state["models"] = merge(catalog, state["models"])
            state["fetched_at"] = now_iso()
            save(state, path)
        except Exception:
            if not state["models"]:
                raise
    pruned = [m for m in state["models"] if is_chat_like(m)]
    if pruned != state["models"]:
        state["models"] = pruned
        save(state, path)
    if not state["models"]:
        raise RuntimeError("no free models available")
    return state["models"]


def complete(prompt: str, *, timeout: int = 30, refresh_hours: float = 24, path: Path = STATE_PATH) -> str:
    models = ranked_models(refresh_hours=refresh_hours, timeout=timeout, path=path)
    errors = []
    for model in list(models):
        ok, elapsed, detail = chat(model, prompt, timeout)
        if ok:
            return detail
        demote(models, model)
        state = load(path)
        state["models"] = models
        save(state, path)
        errors.append(f"{model} ({elapsed:.2f}s): {detail}")
    raise RuntimeError("all models failed:\n" + "\n".join(errors))
