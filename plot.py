# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the file in data/, make one picture, save it to out/.

    uv run plot.py

Three parts, and you will replace all three: rows() reads the file the way *your*
file needs reading, the loop in main() picks the numbers out of it, and the plot at
the bottom is the transformation you chose. Print before you plot.
"""

import csv
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt

FILE = "hko-moonrise-moonset-2026.csv"
PICTURE = "plot.png"

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def time_to_hours(text):
    """Convert HH:MM into decimal hours. Empty cells return None."""
    if not text:
        return None

    hour, minute = text.split(":")
    return int(hour) + int(minute) / 60


def rows(path):
    """Read the HKO moonrise CSV and return its data rows."""
    kept = []

    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        next(reader)  # skip header

        for line in reader:
            if line:
                kept.append(line)

    return kept


def main():
    table = rows(DATA)

    print(f"{DATA.name}: {len(table)} rows")
    print(f"First row: {table[0]}")

    days = []
    moonrise = []
    transit = []
    moonset = []

    for date_text, rise_text, transit_text, set_text in table:
        date = datetime.strptime(date_text, "%Y-%m-%d")
        day_of_year = date.timetuple().tm_yday

        rise = time_to_hours(rise_text)
        transit_time = time_to_hours(transit_text)
        set_time = time_to_hours(set_text)

        if rise is not None:
            days.append(day_of_year)
            moonrise.append(rise)
        else:
            moonrise.append(None)

        transit.append(transit_time)
        moonset.append(set_time)

    all_days = [
        datetime.strptime(row[0], "%Y-%m-%d").timetuple().tm_yday
        for row in table
    ]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.scatter(all_days, moonrise, s=10, label="Moonrise")
    ax.scatter(all_days, transit, s=10, label="Moon transit")
    ax.scatter(all_days, moonset, s=10, label="Moonset")

    ax.set_xlabel("Day of 2026")
    ax.set_ylabel("Time of day (hours)")
    ax.set_title("Moonrise, Transit and Moonset in Hong Kong — 2026")

    ax.set_ylim(0, 24)
    ax.set_yticks(range(0, 25, 3))
    ax.legend()

    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)

    print(f"saved out/{PICTURE}")

    plt.show()


if __name__ == "__main__":
    main()