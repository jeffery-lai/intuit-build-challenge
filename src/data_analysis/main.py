# src/data_analysis/main.py

from __future__ import annotations
from pathlib import Path

from .data_analyzer import load_sales, SalesDataAnalyzer


def main() -> None:
    # Build path to the sales data file
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "data" / "sales.csv"

    records = load_sales(csv_path)
    analyzer = SalesDataAnalyzer(records)

    # 1. Total revenue
    print(f"Total revenue: {analyzer.total_revenue():.2f}\n")

    # 2. Revenue by region
    print("Revenue by region:")
    for region, rev in analyzer.revenue_by_region().items():
        print(f"  {region}: {rev:.2f}")
    print()

    # 3. Top 3 products by revenue
    print("Top 3 products by revenue:")
    for product, rev in analyzer.top_n_products_by_revenue(3):
        print(f"  {product}: {rev:.2f}")
    print()

    # 4. Quantity by category
    print("Quantity by category:")
    for cat, qty in analyzer.quantity_by_category().items():
        print(f"  {cat}: {qty}")
    print()

    # 5. Average order value by date
    print("Average order value by date:")
    for d, avg in sorted(analyzer.average_order_value_by_date().items()):
        print(f"  {d}: {avg:.2f}")
    print()

    # 6. Revenue by region then category
    print("Revenue by region -> category:")
    for region, cat_map in analyzer.revenue_by_region_then_category().items():
        print(f"  Region: {region}")
        for cat, rev in cat_map.items():
            print(f"    {cat}: {rev:.2f}")
    print()

    # 7. Best-selling product
    best = analyzer.best_selling_product_by_quantity()
    if best is not None:
        print(f"Best-selling product by quantity: {best}")
    else:
        print("No data to determine best-selling product.")


if __name__ == "__main__":
    main()
