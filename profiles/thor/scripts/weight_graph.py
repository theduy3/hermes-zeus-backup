#!/usr/bin/env python3
"""Generate a weight trend graph from weight-log.csv and save as weight-graph.png."""
import csv
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

BASE = "/home/hermes/.hermes/profiles/thor/logs"
LOG_FILE = os.path.join(BASE, "weight-log.csv")
OUTPUT = os.path.join(BASE, "weight-graph.png")

def main():
    dates, weights = [], []
    with open(LOG_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            dates.append(datetime.strptime(row["date"], "%Y-%m-%d"))
            weights.append(float(row["weight_kg"]))

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    # Plot line + markers
    ax.plot(dates, weights, color='#00d4ff', linewidth=2.5, marker='o',
            markersize=8, markerfacecolor='#ff6b6b', markeredgecolor='white',
            markeredgewidth=1.5, zorder=5)

    # Annotate each point with the weight
    for d, w in zip(dates, weights):
        ax.annotate(f'{w:.1f}', (d, w), textcoords="offset points",
                    xytext=(0, 14), ha='center', fontsize=9,
                    color='#e0e0e0', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#16213e',
                              edgecolor='#00d4ff', alpha=0.8))

    # Styling
    ax.set_title("Weight Trend", color='white', fontsize=16, fontweight='bold', pad=15)
    ax.set_ylabel("Weight (kg)", color='#e0e0e0', fontsize=11)
    ax.tick_params(colors='#a0a0a0', labelsize=10)
    # X-axis formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    fig.autofmt_xdate(rotation=30)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    if len(dates) > 1:
        ax.set_xlim(dates[0], dates[-1])
    else:
        ax.set_xlim(dates[0] - timedelta(days=2), dates[0] + timedelta(days=2))

    # Grid
    ax.grid(True, linestyle='--', alpha=0.25, color='#a0a0a0')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#333')
    ax.spines['bottom'].set_color('#333')

    # Y-axis padding
    if len(weights) > 1:
        y_min, y_max = min(weights), max(weights)
        pad = max((y_max - y_min) * 0.2, 0.5)
        ax.set_ylim(y_min - pad, y_max + pad)
    else:
        ax.set_ylim(weights[0] - 1, weights[0] + 1)

    plt.tight_layout()
    fig.savefig(OUTPUT, dpi=150, facecolor=fig.get_facecolor())
    print(f"Saved to {OUTPUT}")

if __name__ == "__main__":
    main()
