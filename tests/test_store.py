from orfree.store import PROJECT_ROOT, STATE_PATH, project_root


def test_state_file_lives_in_orfree_project():
    root = project_root()
    assert root.name == "openrouter-free"
    assert (root / "pyproject.toml").is_file()
    assert 'name = "orfree"' in (root / "pyproject.toml").read_text(encoding="utf-8")
    assert STATE_PATH == root / "models.yml"
    assert PROJECT_ROOT == root
    assert "agent-server" not in STATE_PATH.parts
