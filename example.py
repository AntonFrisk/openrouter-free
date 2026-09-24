# Example usage of the orfree package.

import random
import orfree

PROMPTS = [
    "What is the capital of France?",
    "Explain photosynthesis in one sentence.",
    "Name three primary colors.",
    "What is 17 times 24?",
    "Write a haiku about rain in Malmö.",
]

BLUE, RESET = "\033[96m", "\033[0m"  # bright cyan / light blue
prompt = random.choice(PROMPTS) # pick a random prompt from the list.
print(f"Prompt:\n'{BLUE}{prompt}{RESET}' \n")
print("~ sending prompt to free openrouter model ⏳ ~") # waiting for the model to respond.
result = orfree.complete(prompt, include_metadata=True) # metadata is off by default. Set to True to get the model, elapsed time, and failed models.
print(f"Answer:\n'{BLUE}{result['text']}{RESET}' \n")
print("Metadata")
print(f"  model:   {result['model']}")
print(f"  elapsed: {result['elapsed']:.2f}s")
if result["failed"]:
    print("  failed:")
    for f in result["failed"]:
        print(f"    - {f['model']} ({f['elapsed']:.2f}s): {f['error']}")
else:
    print("  failed:  none")
