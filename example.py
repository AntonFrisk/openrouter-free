# Example usage of the orfree package.

from orfree import complete

prompt = "What is the capital of France?"
print(f"Prompt: {prompt}")
print("sending to free openrouter model...")
print(complete(prompt))
