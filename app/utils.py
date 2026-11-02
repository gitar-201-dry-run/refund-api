"""Shared helpers for money and identifiers."""

import re
import secrets

# --- money -----------------------------------------------------------------

CURRENCY_SYMBOLS = {"usd": "$", "eur": "EUR ", "gbp": "GBP "}
MAX_CHARGE_CENTS = 100_000_00  # $100,000.00


def format_cents(amount_cents: int, currency: str = "usd") -> str:
    """Render an integer amount of cents for display, e.g. 5000 -> "$50.00"."""
    symbol = CURRENCY_SYMBOLS.get(currency.lower(), currency.upper() + " ")
    sign = "-" if amount_cents < 0 else ""
    dollars, cents = divmod(abs(amount_cents), 100)
    return f"{sign}{symbol}{dollars:,}.{cents:02d}"


def parse_dollars(text: str) -> int:
    """Parse a string such as "12.50" or "$1,200" into integer cents."""
    cleaned = text.strip().lstrip("$").replace(",", "")
    if not re.fullmatch(r"\d+(\.\d{1,2})?", cleaned):
        raise ValueError(f"Not a valid dollar amount: {text!r}")
    whole, _, frac = cleaned.partition(".")
    return int(whole) * 100 + int(frac.ljust(2, "0") or "0")


def is_valid_charge_amount(amount_cents: int) -> bool:
    return 0 < amount_cents <= MAX_CHARGE_CENTS


def split_evenly(amount_cents: int, parts: int) -> list[int]:
    """Split an amount into `parts` shares that always add up to the total."""
    if parts <= 0:
        raise ValueError("parts must be positive")
    base, remainder = divmod(amount_cents, parts)
    return [base + (1 if i < remainder else 0) for i in range(parts)]


# --- identifiers -----------------------------------------------------------

ID_PREFIXES = {"charge": "ch", "refund": "re"}
_ID_PATTERN = re.compile(r"^(ch|re)_[0-9a-f]{16}$")


def new_id(kind: str) -> str:
    """Generate an opaque id such as ch_3f9a1c0b7d2e4a65."""
    try:
        prefix = ID_PREFIXES[kind]
    except KeyError:
        raise ValueError(f"Unknown id kind: {kind!r}") from None
    return f"{prefix}_{secrets.token_hex(8)}"


def is_valid_id(value: str) -> bool:
    return bool(_ID_PATTERN.match(value))


def id_kind(value: str) -> str | None:
    """Return "charge" or "refund" for a well-formed id, otherwise None."""
    if not is_valid_id(value):
        return None
    prefix = value.split("_", 1)[0]
    for kind, known in ID_PREFIXES.items():
        if known == prefix:
            return kind
    return None
