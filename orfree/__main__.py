"""CLI: uv run python -m orfree 'your prompt'."""
import sys

from orfree.client import complete


def main() -> None:
    prompt = " ".join(sys.argv[1:]) or "Respond with Hello World!"
    print(complete(prompt))


if __name__ == "__main__":
    main()
