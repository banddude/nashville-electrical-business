#!/usr/bin/env python3
"""Generate updated financial charts for the Nashville Sparks business plan."""

from __future__ import annotations

from pathlib import Path
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.patheffects as path_effects

OUTPUT_DIR = Path(__file__).resolve().parent

plt.rcParams['font.family'] = 'Comic Sans MS'

def currency_formatter(value: float, _tick_position: float) -> str:
    """Format currency values in thousands for axis ticks."""
    return f"${value/1000:.0f}K"

def annotate_bars(ax: plt.Axes, bars: list[plt.Rectangle], formatter) -> None:
    """Attach a value label to each bar in *bars* on the supplied *ax*."""
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            formatter(height),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="semibold",
        )

def format_currency(value: float) -> str:
    """Return a human-friendly currency string rounded to the nearest dollar."""
    return f"${int(value):,}"

def format_percent(value: float) -> str:
    """Return a percentage string with one decimal place."""
    return f"{value:.1f}%"

def revenue_cost_profit_chart(projections_data) -> None:
    crews = ["1 Crew", "2 Crews", "3 Crews", "4 Crews"]
    revenue = np.array([
        float(projections_data[19][4].replace('$', '').replace(',', '')),
        float(projections_data[19][6].replace('$', '').replace(',', '')),
        float(projections_data[19][8].replace('$', '').replace(',', '')),
        float(projections_data[19][10].replace('$', '').replace(',', '')),
    ])
    costs = np.array([
        float(projections_data[18][4].replace('$', '').replace(',', '')),
        float(projections_data[18][6].replace('$', '').replace(',', '')),
        float(projections_data[18][8].replace('$', '').replace(',', '')),
        float(projections_data[18][10].replace('$', '').replace(',', '')),
    ])
    profit = np.array([
        float(projections_data[20][4].replace('$', '').replace(',', '')),
        float(projections_data[20][6].replace('$', '').replace(',', '')),
        float(projections_data[20][8].replace('$', '').replace(',', '')),
        float(projections_data[20][10].replace('$', '').replace(',', '')),
    ])

    x = np.arange(len(crews))
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 5))
    
    path_effect = path_effects.withTickedStroke(angle=-90, spacing=7, length=2)

    bars_revenue = ax.bar(x - width, revenue, width, label="Revenue", color="#1f77b4", path_effects=[path_effect])
    bars_costs = ax.bar(x, costs, width, label="Costs", color="#d62728", path_effects=[path_effect])
    bars_profit = ax.bar(x + width, profit, width, label="Profit", color="#4CAF50", path_effects=[path_effect])

    ax.set_ylabel("Monthly Amount")
    ax.set_title("Monthly Revenue, Costs, and Profit by Crew Count")
    ax.set_xticks(x)
    ax.set_xticklabels(crews)
    ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    ax.legend(frameon=False)
    ax.set_ylim(0, 130000)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    annotate_bars(ax, bars_revenue, format_currency)
    annotate_bars(ax, bars_costs, format_currency)
    annotate_bars(ax, bars_profit, format_currency)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "revenue_chart.png", bbox_inches="tight")
    plt.close(fig)

def profit_margin_chart(projections_data) -> None:
    crews = ["1 Crew", "2 Crews", "3 Crews", "4 Crews"]
    revenue = np.array([
        float(projections_data[19][4].replace('$', '').replace(',', '')),
        float(projections_data[19][6].replace('$', '').replace(',', '')),
        float(projections_data[19][8].replace('$', '').replace(',', '')),
        float(projections_data[19][10].replace('$', '').replace(',', '')),
    ])
    profit = np.array([
        float(projections_data[20][4].replace('$', '').replace(',', '')),
        float(projections_data[20][6].replace('$', '').replace(',', '')),
        float(projections_data[20][8].replace('$', '').replace(',', '')),
        float(projections_data[20][10].replace('$', '').replace(',', '')),
    ])
    profit_margin = (profit / revenue) * 100

    x = np.arange(len(crews))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    
    path_effect = path_effects.withTickedStroke(angle=-90, spacing=7, length=2)
    
    bars = ax.bar(x, profit_margin, color="#9467bd", width=0.55, path_effects=[path_effect])

    ax.set_ylabel("Net Profit Margin (%)")
    ax.set_title("Net Profit Margin by Crew Count")
    ax.set_xticks(x)
    ax.set_xticklabels(crews)
    ax.set_ylim(0, 55)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    annotate_bars(ax, bars, format_percent)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "profit_margin_chart.png", bbox_inches="tight")
    plt.close(fig)

def cost_breakdown_chart(projections_data) -> None:
    categories = [row[1] for row in projections_data[9:18]]
    amounts = [float(row[10].replace('$', '').replace(',', '')) for row in projections_data[9:18]]

    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax.set_title("Cost Breakdown – 4 Crew Full Operation")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "cost_breakdown.png", bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    with open('BIBLE/Nashville Electrical Business Plan - Projections.csv', 'r') as f:
        reader = csv.reader(f)
        projections_data = list(reader)

    revenue_cost_profit_chart(projections_data)
    profit_margin_chart(projections_data)
    cost_breakdown_chart(projections_data)
    print("Charts regenerated successfully.")
