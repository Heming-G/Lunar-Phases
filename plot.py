# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the file in data/, make one picture, save it to out/.

    uv run plot.py

The saved HKO CSV supplies dates and event times. Missing cells remain gaps.
Dots avoid connecting events across midnight.
"""

import csv
from pathlib import Path
from datetime import datetime
import matplotlib.dates as mdates

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

    dates = []
    moonrise = []
    transit = []
    moonset = []

    for date_text, rise_text, transit_text, set_text in table:
        dates.append(datetime.strptime(date_text, "%Y-%m-%d"))
        # Keep one entry per date. Missing events remain gaps, not zeroes.
        moonrise.append(time_to_hours(rise_text))
        transit.append(time_to_hours(transit_text))
        moonset.append(time_to_hours(set_text))

    background = "#101925"
    text_color = "#e8edf3"
    muted = "#a5b4c5"
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=background)
    ax.set_facecolor(background)

    ax.scatter(dates, moonrise, s=13, color="#edc77e", label="Moonrise", linewidths=0)
    ax.scatter(dates, transit, s=13, color="#b6a4df", label="Moon transit", linewidths=0)
    ax.scatter(dates, moonset, s=13, color="#83cbd2", label="Moonset", linewidths=0)

    fig.text(0.09, 0.92, "LUNAR RHYTHM", color=text_color, fontsize=27, weight="bold")
    fig.text(0.09, 0.875, "Hong Kong / 2026   —   Daily moonrise, transit and moonset",
             color=muted, fontsize=12)
    ax.set_xlim(datetime(2026, 1, 1), datetime(2026, 12, 31))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_ylim(0, 24)
    ax.set_yticks(range(0, 25, 3))
    ax.set_yticklabels([f"{hour:02d}:00" for hour in range(0, 25, 3)])
    ax.set_ylabel("Time of day · Hong Kong time (UTC+8)", color=muted, labelpad=15)
    ax.tick_params(colors=muted, length=0, pad=10)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#344150", linewidth=0.6, alpha=0.6)
    for spine in ax.spines.values():
        spine.set_visible(False)
    legend = ax.legend(loc="lower left", bbox_to_anchor=(0, 1.025), ncol=3,
                       frameon=False, borderaxespad=0, fontsize=11)
    for label in legend.get_texts():
        label.set_color(text_color)
    fig.text(0.09, 0.045,
             "Each dot is one daily event. Midnight wraps from 24:00 to 00:00; blank records remain gaps.",
             color=muted, fontsize=10)
    fig.text(0.09, 0.018, "Source: Hong Kong Observatory · MRS Open Data · 365 daily records",
             color=muted, fontsize=9)
    fig.subplots_adjust(left=0.09, right=0.975, bottom=0.13, top=0.76)

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=180, facecolor=background)
    plt.close(fig)

    print(f"saved out/{PICTURE}")



if __name__ == "__main__":
    main()