# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for custom decimal.Decimal subclasses in qbraid_core.

"""
from decimal import Decimal

from qbraid_core.decimal import USD, Credits


def test_credits_initialization():
    """Test initialization of Credits."""
    c = Credits("1000")
    assert isinstance(c, Decimal)
    assert repr(c) == "Credits('1000')"
    assert str(c) == "1000"
    assert int(c) == 1000
    assert float(c) == 1000.0


def test_usd_initialization():
    """Test initialization of USD."""
    u = USD("10")
    assert isinstance(u, Decimal)
    assert repr(u) == "USD('10')"
    assert str(u) == "10"
    assert int(u) == 10
    assert float(u) == 10.0


def test_credits_to_usd():
    """Test conversion from Credits to USD."""
    credits = Credits("1000")
    usd = credits.to_usd()
    assert isinstance(usd, USD)
    assert repr(usd) == "USD('10')"


def test_usd_to_credits():
    """Test conversion from USD to Credits."""
    usd = USD("10")
    credits = usd.to_credits()
    assert isinstance(credits, Credits)
    assert repr(credits) == "Credits('1000')"


def test_bidirectional_conversion():
    """Test that converting back and forth maintains value."""
    credits = Credits("1000")
    usd = credits.to_usd()
    credits_back = usd.to_credits()
    assert credits == credits_back
