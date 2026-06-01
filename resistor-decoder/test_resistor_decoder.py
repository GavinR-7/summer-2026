from resistor_decoder import (
    band_to_digit, decode_resistance, format_resistance, band_to_tolerance,
    InvalidColorError, InvalidNumberOfColorsError,
)
import pytest

# Multiple decode cases - different multipliers and tolerances
@pytest.mark.parametrize("bands,expected_ohms,expected_tol", [
    (["brown", "black", "red", "gold"],   1000.0, 5.0),
    (["brown", "black", "black", "gold"], 10.0,   5.0),
    (["red", "red", "brown", "silver"],   220.0, 10.0),
    (["yellow", "violet", "orange", "brown"], 47000.0, 1.0),
])
def test_decode_various(bands, expected_ohms, expected_tol):
    ohms, tol = decode_resistance(bands)
    assert ohms == expected_ohms
    assert tol == expected_tol

# Test the formatter in isolation - no decode involved
@pytest.mark.parametrize("ohms,tol,expected", [
    (1000.0,  5.0,  "1.0 kΩ ±5%"),
    (220.0,  10.0,  "220 Ω ±10%"),
    (47000.0, 1.0,  "47.0 kΩ ±1%"),
])
def test_format_resistance(ohms, tol, expected):
    assert format_resistance(ohms, tol) == expected

# Sneaky one: orange is a valid color but NOT a valid tolerance
def test_band_to_tolerance_rejects_digit_only_colors():
    with pytest.raises(InvalidColorError):
        band_to_tolerance("orange")