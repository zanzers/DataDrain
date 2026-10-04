import re

UNITS = {
    "kb": 1000,
    "mb": 1000**2,
    "gb": 1000**3,
    "tb": 1000**4,
}


def parse_data(text: str) -> int:
    
    text = text.strip().lower()

    match = re.match(r"^(\d+(?:\.\d+)?)\s*([a-z]+)$", text)
    if not match:
        raise ValueError("Use a format like 2 GB or 2.56 GB")

    number = float(match.group(1))
    unit = match.group(2)

    if unit not in UNITS:
        raise ValueError(f"Unknown unit: {unit}")
    if number <= 0:
        raise ValueError("Amount mush be greater than 0")
    
    return int(number * UNITS[unit])
