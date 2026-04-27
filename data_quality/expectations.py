"""Optional Great Expectations suite definitions.

Kept lightweight and importable even when great_expectations isn't installed.
"""
from __future__ import annotations

EVENT_EXPECTATIONS: dict = {
    "expectations": [
        {"type": "expect_column_to_exist", "kwargs": {"column": "event_id"}},
        {"type": "expect_column_values_to_not_be_null", "kwargs": {"column": "event_id"}},
        {"type": "expect_column_values_to_be_unique", "kwargs": {"column": "event_id"}},
        {
            "type": "expect_column_values_to_be_in_set",
            "kwargs": {"column": "event_type", "value_set": ["view", "cart", "purchase"]},
        },
        {
            "type": "expect_column_values_to_be_between",
            "kwargs": {"column": "quantity", "min_value": 1, "max_value": 100},
        },
    ]
}
