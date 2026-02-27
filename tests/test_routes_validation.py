import pytest

from app.api.routes import _parse_amount, _parse_currency
from app.errors import ValidationError


def test_parse_currency_normalizes():
    assert _parse_currency(" usd ", field="base") == "USD"


def test_parse_currency_rejects_invalid():
    with pytest.raises(ValidationError):
        _parse_currency("USDX", field="base")


def test_parse_amount_accepts_decimal_comma():
    assert _parse_amount("10,5") == 10.5


def test_parse_amount_rejects_missing():
    with pytest.raises(ValidationError):
        _parse_amount(None)


def test_parse_amount_rejects_non_positive():
    with pytest.raises(ValidationError):
        _parse_amount("0")
