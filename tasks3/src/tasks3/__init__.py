# tasks3/src/tasks3/__init__.py

def inc(n: int) -> int:
    return n + 1

def main() -> None:
    print("tasks3 running")
    from .cli import main as cli_main
    raise SystemExit(cli_main())
