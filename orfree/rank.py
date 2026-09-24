"""Move a failed model down the ranked list."""


def demote(models: list[str], model: str, steps: int = 2) -> list[str]:
    try:
        i = models.index(model)
    except ValueError:
        return models
    models.pop(i)
    models.insert(min(i + steps, len(models)), model)
    return models
