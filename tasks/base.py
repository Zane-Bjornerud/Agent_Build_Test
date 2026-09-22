from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class Example:
    id: str
    input: Any
    expected: Any

@dataclass
class Task:
    name: str
    examples: list[Example]
    run: Callable            # (provider, Example) -> (parsed, Call)
    score: Callable          # (expected, parsed) -> dict[str, float]