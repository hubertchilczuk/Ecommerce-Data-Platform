"""Generate synthetic e-commerce events (view / cart / purchase)."""
from __future__ import annotations

import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import click

from .config import GeneratorConfig
from .schemas import Event, EventType, Product


def _build_catalog(cfg: GeneratorConfig) -> list[Product]:
    return [
        Product(
            product_id=f"P{idx:05d}",
            category=random.choice(cfg.categories),
            price=round(random.uniform(5, 500), 2),
        )
        for idx in range(cfg.num_products)
    ]


def generate_events(cfg: GeneratorConfig) -> list[Event]:
    random.seed(cfg.seed)
    catalog = _build_catalog(cfg)
    users = [f"U{idx:06d}" for idx in range(cfg.num_users)]
    now = datetime.now(timezone.utc)

    events: list[Event] = []
    for _ in range(cfg.num_events):
        event_type = random.choices(list(EventType), weights=cfg.event_weights, k=1)[0]
        product = random.choice(catalog)
        quantity = random.randint(1, 3) if event_type != EventType.VIEW else 1
        revenue = round(product.price * quantity, 2) if event_type == EventType.PURCHASE else None

        events.append(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=event_type,
                event_time=now - timedelta(seconds=random.randint(0, 7 * 24 * 3600)),
                user_id=random.choice(users),
                session_id=str(uuid.uuid4()),
                product=product,
                quantity=quantity,
                revenue=revenue,
            )
        )
    return events


def write_jsonl(events: list[Event], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for ev in events:
            f.write(ev.model_dump_json() + "\n")
    return out


@click.command()
@click.option("--events", "num_events", default=10_000, show_default=True)
@click.option("--output", default="data/raw/events.jsonl", show_default=True)
@click.option("--seed", default=42, show_default=True)
def main(num_events: int, output: str, seed: int) -> None:
    cfg = GeneratorConfig(num_events=num_events, output_path=output, seed=seed)
    events = generate_events(cfg)
    path = write_jsonl(events, cfg.output_path)
    click.echo(f"Wrote {len(events)} events to {path}")


if __name__ == "__main__":
    main()
