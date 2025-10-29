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
    return f"${value:,.0f}"

def format_percent(value: float) -> str:
    """Return a percentage string with one decimal place."""
    return f"{value:.1f}%"

def revenue_cost_profit_chart(data) -> None:
    crews = [f"{i} Crew" + ("s" if i > 1 else "") for i in data.keys()]
    revenue = np.array([d['monthly_revenue'] for d in data.values()])
    costs = np.array([d['monthly_costs'] for d in data.values()])
    profit = np.array([d['monthly_profit'] for d in data.values()])

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

def profit_margin_chart(data) -> None:
    crews = [f"{i} Crew" + ("s" if i > 1 else "") for i in data.keys()]
    profit_margin = np.array([float(d['profit_margin'].strip('%')) for d in data.values()])

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

def cost_breakdown_chart() -> None:
    categories = [
        "Licensing/Insurance",
        "Vehicles",
        "Marketing",
        "Office",
        "Consumables",
        "Technician Labor",
        "Apprentice Labor",
        "Admin Labor",
        "Project Manager",
        "Contingency",
    ]
    amounts = np.array([1028, 3985, 2000, 1967, 269, 22917, 18333, 3333, 11111, 22000])

    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax.set_title("Cost Breakdown – 4 Crew Full Operation")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "cost_breakdown.png", bbox_inches="tight")
    plt.close(fig)

def main() -> None:
    with open('business_plan_data.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)

    crew_data = {}
    for row in data:
        crew_count = int(row[0])
        crew_data[crew_count] = {
            'monthly_revenue': float(row[1]),
            'monthly_costs': float(row[2]),
            'monthly_profit': float(row[3]),
            'profit_margin': row[4]
        }

    revenue_cost_profit_chart(crew_data)
    profit_margin_chart(crew_data)
    cost_breakdown_chart()
    print("Charts regenerated successfully.")


if __name__ == "__main__":
    main()