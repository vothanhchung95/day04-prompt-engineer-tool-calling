import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.agent.agent import run_chat


def main():
    run_chat()


if __name__ == "__main__":
    main()
