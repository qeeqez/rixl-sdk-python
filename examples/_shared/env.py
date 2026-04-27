import os
import sys


def must_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"missing {name}")
    return value
