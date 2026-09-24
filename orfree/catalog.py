"""Fetch OpenRouter free text models and merge into a ranked list."""
from __future__ import annotations

import requests

MODELS_URL = "https://openrouter.ai/api/v1/models"
PARAMS = {
    "output_modalities": "text",
    "input_modalities": "text",
    "sort": "latency-low-to-high",
    "max_price": 0,
}

# Classifiers, guardrails, and embeddings return labels, not chat replies.
_SKIP = (
    "content-safety",
    "content_safety",
    "content safety",
    "guardrail",
    "moderation",
    "embedding",
    "rerank",
    "classifier",
)


def is_chat_like(model: dict | str) -> bool:
    if isinstance(model, str):
        mid, name, desc = model, "", ""
    else:
        mid = model.get("id") or ""
        name = model.get("name") or ""
        desc = model.get("description") or ""
    hay = f"{mid} {name} {desc}".lower()
    if any(s in hay for s in _SKIP):
        return False
    parts = mid.lower().split(":")[0].replace("/", "-").split("-")
    return "embed" not in parts


def fetch_catalog(api_key: str, timeout: int = 30) -> list[str]:
    resp = requests.get(
        MODELS_URL,
        params=PARAMS,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=timeout,
    )
    resp.raise_for_status()
    ids = []
    for m in resp.json().get("data") or []:
        mid = m.get("id") or ""
        if mid.endswith(":free") and mid != "openrouter/free" and is_chat_like(m):
            ids.append(mid)
    return ids


def merge(catalog: list[str], ranked: list[str]) -> list[str]:
    catalog_set = set(catalog)
    kept = [m for m in ranked if m in catalog_set]
    return kept + [m for m in catalog if m not in kept]
