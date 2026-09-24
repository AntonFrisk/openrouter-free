from unittest.mock import Mock, patch

from orfree.catalog import fetch_catalog, is_chat_like, merge


def test_merge_keeps_local_order_and_appends_new():
    catalog = ["fast", "mid", "slow", "new"]
    ranked = ["slow", "fast"]
    assert merge(catalog, ranked) == ["slow", "fast", "mid", "new"]


def test_merge_drops_gone_ids():
    catalog = ["a", "c"]
    ranked = ["b", "a", "gone"]
    assert merge(catalog, ranked) == ["a", "c"]


def test_merge_empty_ranked_uses_catalog():
    catalog = ["a", "b"]
    assert merge(catalog, []) == ["a", "b"]


def test_fetch_catalog_keeps_free_chat_slugs_only():
    payload = {
        "data": [
            {"id": "nvidia/fast:free"},
            {"id": "openrouter/free"},
            {"id": "openai/gpt-4o"},
            {"id": "inclusionai/ling:free"},
            {
                "id": "nvidia/nemotron-3.5-content-safety:free",
                "name": "Nemotron Content Safety",
                "description": "A compact guardrail model that moderates LLM inputs.",
            },
            {"id": "nvidia/nemotron-3-embed-1b:free"},
        ]
    }
    fake = Mock()
    fake.json.return_value = payload
    fake.raise_for_status = Mock()
    with patch("orfree.catalog.requests.get", return_value=fake) as get:
        ids = fetch_catalog("sk-test")
    assert ids == ["nvidia/fast:free", "inclusionai/ling:free"]
    get.assert_called_once()


def test_is_chat_like_rejects_safety_and_embed_slugs():
    assert is_chat_like("nvidia/nemotron-3.5-lightning:free")
    assert not is_chat_like("nvidia/nemotron-3.5-content-safety:free")
    assert not is_chat_like("nvidia/nemotron-3-embed-1b:free")

