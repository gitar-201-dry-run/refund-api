import pytest

from app.utils import format_cents, id_kind, new_id, parse_dollars, split_evenly


def test_format_cents():
    assert format_cents(5000) == "$50.00"
    assert format_cents(123456789) == "$1,234,567.89"
    assert format_cents(-250) == "-$2.50"


@pytest.mark.parametrize("text,expected", [("12.50", 1250), ("$1,200", 120000), ("0.5", 50)])
def test_parse_dollars(text, expected):
    assert parse_dollars(text) == expected


def test_parse_dollars_rejects_garbage():
    with pytest.raises(ValueError):
        parse_dollars("12.345")


def test_split_evenly_preserves_total():
    shares = split_evenly(1000, 3)
    assert sum(shares) == 1000
    assert shares == [334, 333, 333]


def test_ids_round_trip():
    assert id_kind(new_id("charge")) == "charge"
    assert id_kind(new_id("refund")) == "refund"
    assert id_kind("nope") is None
