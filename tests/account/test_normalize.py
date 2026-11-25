"""The shared raw-attribute gate every account country's normalizer uses."""

from __future__ import annotations

import pytest

from custom_components.gls.account.normalize import pick, scalar, text


@pytest.mark.parametrize("value", [None, "x", 0, 1.5, True])
def test_scalars_are_accepted(value):
    """Accept only the supported scalar types for safe account attributes."""
    assert scalar(value) is True


@pytest.mark.parametrize("value", [float("inf"), float("nan"), {}, [], b"x"])
def test_non_finite_and_nested_values_are_refused(value):
    """Reject nested containers and non-finite values from published attributes."""
    assert scalar(value) is False


def test_text_keeps_only_nonempty_strings():
    """Trim meaningful text and discard blank strings or non-string values."""
    assert text("  Hello ") == "Hello"
    assert text("   ") is None
    assert text(7) is None


def test_pick_keeps_only_allowlisted_scalars():
    """Copy only allowlisted fields that also pass scalar validation."""
    source = {"keep": "a", "nested": {"pin": "1"}, "drop": "b", "bad": float("nan")}
    assert pick(source, frozenset({"keep", "nested", "bad"})) == {"keep": "a"}
