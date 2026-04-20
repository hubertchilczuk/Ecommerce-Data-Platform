"""Configuration for the event generator."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GeneratorConfig:
    num_events: int = 10_000
    num_users: int = 1_000
    num_products: int = 200
    categories: list[str] = field(
        default_factory=lambda: ["electronics", "fashion", "home", "sports", "books"]
    )
    # Probability weights for view / cart / purchase
    event_weights: tuple[float, float, float] = (0.7, 0.2, 0.1)
    seed: int = 42
    output_path: str = "data/raw/events.jsonl"
