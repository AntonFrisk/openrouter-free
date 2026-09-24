# openrouter-free

Demo for getting access to openrouter free models and maintaining a self-healing list of models to use.

Self-healing OpenRouter client. It keeps a ranked list of **free** text models (lowest-latency first), sends chat to the top model, and on timeout or error tries the next while demoting the failure two steps.

Catalog comes from the [OpenRouter Models API](https://openrouter.ai/docs/guides/overview/models). Refresh happens every 24 hours (to avoid double API calls on each prompt). 
Enjoy!

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



## Run the example

Run the `example.py` do quick-test it.

Example run where a model failed and was dropped     from the list.

```bash
name@laptop MINGW64 ~/Documents/code/openrouter-free (main)
$ uv run example.py 
Prompt:
'Explain photosynthesis in one sentence.'

⏳ sending prompt to free openrouter model...
Answer:
'Photosynthesis is the process by which green plants, algae, and certain bacteria convert sunlight into chemical energy, producing glucose while releasing oxygen from carbon dioxide and water.'

Metadata:
  model:   nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
  elapsed: 4.23s
  failed:
    - poolside/laguna-xs-2.1:free (0.65s): Provider returned error
```

