#!/usr/bin/env python3
"""Generate updated financial charts for the Nashville Sparks business plan."""

from __future__ import annotations

from pathlib import Path

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


def revenue_cost_profit_chart() -> None:
    crews = ["1 Crew", "2 Crews", "3 Crews", "4 Crews"]
    revenue = np.array([32083, 64167, 91042, 117917])
    costs = np.array([18837, 35971, 59121, 86943])
    profit = np.array([13246, 28196, 31920, 30974])

    x = np.arange(len(crews))
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 5))
    
    path_effect = path_effects.withTickedStroke(angle=-90, spacing=7, length=2)

    bars_revenue = ax.bar(x - width, revenue, width, label="Revenue", color="#1f77b4", path_effects=[path_effect])
    bars_costs = ax.bar(x, costs, width, label="Costs", color="#d62728", path_effects=[path_effect])
    bars_profit = ax.bar(x + width, profit, width, label="Profit", color="#2ca02c", path_effects=[path_effect])

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


def profit_margin_chart() -> None:
    crews = ["1 Crew", "2 Crews", "3 Crews", "4 Crews"]
    profit_margin = np.array([41.3, 43.9, 35.1, 26.2])

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
        "Apprentice Labor",
        "Technician Labor",
        "Project Manager",
        "Vehicles",
        "Marketing",
        "Other Operating Costs",
        "Unaccounted Costs",
    ]
    amounts = np.array([18333, 22917, 11111, 3985, 2000, 6597, 22000])

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    
    path_effect = path_effects.withTickedStroke(angle=-90, spacing=7, length=2)
    
    bars = ax.barh(categories, amounts, color="#ff7f0e", path_effects=[path_effect])

    ax.set_xlabel("Monthly Spend")
    ax.set_title("Cost Breakdown – 4 Crew Full Operation")
    ax.xaxis.set_major_formatter(FuncFormatter(currency_formatter))
    ax.grid(axis="x", linestyle="--", alpha=0.35)

    for bar in bars:
        width = bar.get_width()
        ax.annotate(
            format_currency(width),
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=9,
            fontweight="semibold",
        )

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "cost_breakdown.png", bbox_inches="tight")
    plt.close(fig)


def implementation_timeline_chart() -> None:
    phases = [
        ("Foundation & Launch", 1.0, 1.0),
        ("Brand & Marketing", 1.0, 2.0),
        ("Operations Setup", 3.0, 2.0),
        ("Client Acquisition", 5.0, 3.0),
        ("Team Expansion", 8.0, 3.0),
        ("Scaling & Optimization", 11.0, 1.5),
    ]

    milestones = [
        ("Ready to Operate", 2.0),
        ("Marketing Ready", 3.0),
        ("Operational Ready", 5.0),
        ("1 Crew Profitable", 3.0),
        ("2 Crews Operating", 9.0),
        ("4 Crews Live", 12.0),
    ]

    fig, ax = plt.subplots(figsize=(9, 5))
    y_positions = np.arange(len(phases))

    path_effect = path_effects.withTickedStroke(angle=-90, spacing=7, length=2)

    for (label, start, duration), y in zip(phases, y_positions):
        ax.barh(
            y=y,
            width=duration,
            left=start,
            height=0.6,
            align="center",
            color="#17becf",
            edgecolor="black",
            linewidth=0.6,
            path_effects=[path_effect]
        )
        ax.text(
            start + duration / 2,
            y,
            label,
            ha="center",
            va="center",
            fontsize=9,
            fontweight="semibold",
            color="black",
        )

    milestone_y = np.full(len(milestones), len(phases) + 0.2)
    milestone_x = [point for _, point in milestones]
    ax.scatter(milestone_x, milestone_y, marker="v", color="#d62728", s=80, zorder=5)

    for (label, x), y in zip(milestones, milestone_y):
        ax.text(
            x,
            y + 0.15,
            label,
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=45,
        )

    ax.set_yticks([])
    ax.set_xlabel("Month of Year 1")
    ax.set_title("12-Month Implementation Timeline & Milestones")
    ax.set_xlim(1, 13)
    ax.set_xticks(np.arange(1, 13, 1))
    ax.grid(axis="x", linestyle="--", alpha=0.35)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "timeline_chart.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    revenue_cost_profit_chart()
    profit_margin_chart()
    cost_breakdown_chart()
    implementation_timeline_chart()
    print("Charts regenerated successfully.")


if __name__ == "__main__":
    main()
