import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

COLOR_DIGITS = {
    "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
    "green": 5, "blue": 6, "violet": 7, "grey": 8, "white": 9,
}
# Multiplier band uses the same digit as ×10^digit, plus:
#   gold = ×0.1, silver = ×0.01
TOLERANCE = {"brown": 1.0, "red": 2.0, "gold": 5.0, "silver": 10.0}
# A 4-band resistor reads: digit, digit, multiplier, tolerance. 
# So brown black red gold = 1, 0, ×10², ±5% = 1000 Ω = 1.0 kΩ ±5%.

class InvalidNumberOfColorsError(ValueError):
    pass

class InvalidColorError(ValueError):
    pass


def band_to_digit(color: str) -> int:
    """One color → its digit. Raises InvalidColorError."""
    c = color.lower()
    if c not in COLOR_DIGITS:
        raise InvalidColorError(f"This is not a valid color: {color!r}")
    return COLOR_DIGITS[c]

def band_to_tolerance(color: str) -> float:
    """One color → its tolerance. Raises InvalidColorError."""
    c = color.lower()
    if c not in TOLERANCE:
        raise InvalidColorError(f"This is not a valid color: {color!r}")
    return TOLERANCE[c]

def decode_resistance(bands: list[str]) -> tuple[float, float]:
    """4 bands → (ohms, tolerance_percent). Raises on bad input."""
    if len(bands) != 4:
        raise InvalidNumberOfColorsError(f"Invalid amount of color inputs: {bands!r}") 
    fdig = band_to_digit(bands[0])
    sdig = band_to_digit(bands[1])
    tdig = pow(10, band_to_digit(bands[2]))
    tolerance = band_to_tolerance(bands[3])
    ohms = (fdig*10 + sdig)*tdig
    logger.info("Decoded bands %s into %s ohms", bands, ohms)
    return (float(ohms), float(tolerance))


def format_resistance(ohms: float, tolerance: float) -> str:
    """(1000.0, 5.0) → '1.0 kΩ ±5%'. Pure formatting, no logic."""
    if ohms >= 1000:
        fohms = f"{ohms/1000:.1f} kΩ"
    else: 
        fohms = f"{ohms:g} Ω"
    ftol = f" ±{tolerance:g}%"
    return fohms + ftol

def main() -> None:
    bands = sys.argv[1:]
    try:
        ohms, tolerance = decode_resistance(bands)
        result = format_resistance(ohms, tolerance)
        print(result)
    except (InvalidColorError, InvalidNumberOfColorsError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)    

if __name__ == "__main__":
    main()
