# openrouter-free

Demo for getting access to openrouter free models and maintaining a self-healing list of models to use.

Self-healing OpenRouter client. It keeps a ranked list of **free** text models (lowest-latency first), sends chat to the top model, and on timeout or error tries the next while demoting the failure two steps.

Catalog comes from the [OpenRouter Models API](https://openrouter.ai/docs/guides/overview/models), not the website. Refresh happens at most every 24 hours.

## Setup

```bash
uv sync
cp .env.example .env   # then set OPENROUTER_API_KEY
```

Use a dedicated OpenRouter key in this project's `.env`. Do not reuse keys from other projects.

## Use as a library

```python
from orfree import complete

print(complete("Respond with Hello World!"))
```

## CLI

```bash
uv run python -m orfree "Respond with Hello World!"
```

The working list is **only** `models.yml` in this repo. This package never reads or writes another project's files.

## Tests

```bash
uv run pytest
```
