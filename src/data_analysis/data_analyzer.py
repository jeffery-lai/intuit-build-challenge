# src/data_analysis/data_analyzer.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from collections import defaultdict
from typing import Iterable, Dict, List, Optional
import csv


@dataclass
class SalesRecord:
    order_id: str
    date: date
    region: str
    product: str
    category: str
    quantity: int
    unit_price: float

    @property
    def line_revenue(self) -> float:
        return self.quantity * self.unit_price


def load_sales(csv_path: Path) -> List[SalesRecord]:
    """
    Load sales data from a CSV file.
    Uses csv.DictReader and functional-style processing.
    """
    records: List[SalesRecord] = []

    with csv_path.open(newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                yield SalesRecord(
                    order_id=row["order_id"],
                    date=date.fromisoformat(row["date"]),
                    region=row["region"],
                    product=row["product"],
                    category=row["category"],
                    quantity=int(row["quantity"]),
                    unit_price=float(row["unit_price"]),
                )
            except Exception as e:
                print(f"Skipping malformed row {row}: {e}")

    return records


class SalesDataAnalyzer:
    """
    Performs various aggregation and grouping operations using
    functional constructs in Python.
    """

    def __init__(self, records: Iterable[SalesRecord]) -> None:
        self.records: List[SalesRecord] = list(records)

    # ---------- Aggregation / grouping methods ----------

    def total_revenue(self) -> float:
        """
        Returns the total revenue.
        """
        return sum(r.line_revenue for r in self.records)

    def revenue_by_region(self) -> Dict[str, float]:
        """
        Returns the revenue by region.
        """
        totals: Dict[str, float] = defaultdict(float)
        for r in self.records:
            totals[r.region] += r.line_revenue
        return dict(totals)

    def revenue_by_product(self) -> Dict[str, float]:
        """
        Returns the revenue by product.
        """
        totals: Dict[str, float] = defaultdict(float)
        for r in self.records:
            totals[r.product] += r.line_revenue
        return dict(totals)

    def quantity_by_category(self) -> Dict[str, int]:
        """
        Returns the quantity by category.
        """
        totals: Dict[str, int] = defaultdict(int)
        for r in self.records:
            totals[r.category] += r.quantity
        return dict(totals)

    def average_order_value_by_date(self) -> Dict[date, float]:
        """
        Returns the average order value by date.
        """
        # date -> order_id -> list[SalesRecord]
        by_date_then_order: Dict[date, Dict[str, List[SalesRecord]]] = defaultdict(
            lambda: defaultdict(list)
        )

        for r in self.records:
            by_date_then_order[r.date][r.order_id].append(r)

        result: Dict[date, float] = {}

        for d, orders in by_date_then_order.items():
            order_totals = [
                sum(line.line_revenue for line in order_lines)
                for order_lines in orders.values()
            ]
            avg = (
                sum(order_totals) / len(order_totals)
                if order_totals
                else 0.0
            )
            result[d] = avg

        return result

    def top_n_products_by_revenue(self, n: int) -> List[tuple[str, float]]:
        """
        Returns the top n products by revenue.
        """
        items = list(self.revenue_by_product().items())
        items.sort(key=lambda kv: kv[1], reverse=True)
        return items[:n]

    def revenue_by_region_then_category(self) -> Dict[str, Dict[str, float]]:
        """
        Returns the revenue by region then category.
        """
        nested: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))

        for r in self.records:
            nested[r.region][r.category] += r.line_revenue

        # convert default dicts to plain dicts for nicer printing / testing
        return {region: dict(cat_map) for region, cat_map in nested.items()}

    def best_selling_product_by_quantity(self) -> Optional[str]:
        """
        Returns the product with the highest quantity sold.
        """
        totals: Dict[str, int] = defaultdict(int)
        for r in self.records:
            totals[r.product] += r.quantity

        if not totals:
            return None

        # argmax over totals dict
        return max(totals.items(), key=lambda kv: kv[1])[0]
