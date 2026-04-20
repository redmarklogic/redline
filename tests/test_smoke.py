"""Smoke tests — verify the package imports and basic public API."""

import rl


def test_hello() -> None:
    assert rl.hello() == "Hello from redline!"
