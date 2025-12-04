import csv
from datetime import date
from pathlib import Path

import pytest

from data_analysis.data_analyzer import (
    SalesRecord,
    SalesDataAnalyzer,
    load_sales,
)


def sample_records():
    """
    Create a small fixed dataset for testing:

    Records:
    1) O-001, 2024-01-01, North, Laptop, Electronics, qty=2, price=1000  -> rev=2000
    2) O-002, 2024-01-01, North, Mouse,  Accessories, qty=5, price=20    -> rev=100
    3) O-003, 2024-01-02, South, Laptop, Electronics, qty=1, price=1100 -> rev=1100
    4) O-003, 2024-01-02, South, Mouse,  Accessories, qty=2, price=25   -> rev=50

    For 2024-01-01:
      - Orders: O-001 (2000), O-002 (100) -> avg order value = 1050

    For 2024-01-02:
      - Order: O-003 (1100 + 50 = 1150)   -> avg order value = 1150
    """
    return [
        SalesRecord(
            order_id="O-001",
            date=date(2024, 1, 1),
            region="North",
            product="Laptop",
            category="Electronics",
            quantity=2,
            unit_price=1000.0,
        ),
        SalesRecord(
            order_id="O-002",
            date=date(2024, 1, 1),
            region="North",
            product="Mouse",
            category="Accessories",
            quantity=5,
            unit_price=20.0,
        ),
        SalesRecord(
            order_id="O-003",
            date=date(2024, 1, 2),
            region="South",
            product="Laptop",
            category="Electronics",
            quantity=1,
            unit_price=1100.0,
        ),
        SalesRecord(
            order_id="O-003",
            date=date(2024, 1, 2),
            region="South",
            product="Mouse",
            category="Accessories",
            quantity=2,
            unit_price=25.0,
        ),
    ]


# ---------- Tests for SalesDataAnalyzer ----------

def test_total_revenue():
    records = sample_records()
    analyzer = SalesDataAnalyzer(records)

    # 2000 + 100 + 1100 + 50 = 3250
    assert analyzer.total_revenue() == pytest.approx(3250.0)


def test_revenue_by_region():
    records = sample_records()
    analyzer = SalesDataAnalyzer(records)

    result = analyzer.revenue_by_region()

    # North: 2000 + 100 = 2100
    # South: 1100 + 50 = 1150
    assert result["North"] == pytest.approx(2100.0)
    assert result["South"] == pytest.approx(1150.0)
    assert set(result.keys()) == {"North", "South"}


def test_revenue_by_product():
    records = sample_records()
    analyzer = SalesDataAnalyzer(records)

    result = analyzer.revenue_by_product()

    # Laptop: 2000 + 1100 = 3100
    # Mouse: 100 + 50 = 150
    assert result["Laptop"] == pytest.approx(3100.0)
    assert result["Mouse"] == pytest.approx(150.0)
    assert set(result.keys()) == {"Laptop", "Mouse"}


def test_quantity_by_category():
    records = sample_records()
    analyzer = SalesDataAnalyzer(records)

    result = analyzer.quantity_by_category()

    # Electronics: 2 + 1 = 3
    # Accessories: 5 + 2 = 7
    assert result["Electronics"] == 3
    assert result["Accessories"] == 7
    assert set(result.keys()) == {"Electronics", "Accessories"}


def test_average_order_value_by_date():
    records = sample_records()
    analyzer = SalesDataAnalyzer(records)

    result = analyzer.average_order_value_by_date()

    # 2024-01-01: avg(2000, 100) = 1050
    # 2024-01-02: avg(1150) = 1150
    assert result[date(2024, 1, 1)] == pytest.approx(1050.0)
    assert result[date(2024, 1, 2)] == pytest.approx(1150.0)
    assert set(result.keys()) == {date(2024, 1, 1), date(2024, 1, 2)}


def test_top_n_products_by_revenue():
    records = sample_records()
    analyzer = SalesDataAnalyzer(records)

    top1 = analyzer.top_n_products_by_revenue(1)
    top2 = analyzer.top_n_products_by_revenue(2)

    # Laptop has more revenue than Mouse
    assert len(top1) == 1
    assert top1[0][0] == "Laptop"

    product_names = [name for name, _ in top2]
    assert product_names == ["Laptop", "Mouse"]


def test_revenue_by_region_then_category():
    records = sample_records()
    analyzer = SalesDataAnalyzer(records)

    result = analyzer.revenue_by_region_then_category()

    # North/Electronics: 2000
    # North/Accessories: 100
    # South/Electronics: 1100
    # South/Accessories: 50
    assert result["North"]["Electronics"] == pytest.approx(2000.0)
    assert result["North"]["Accessories"] == pytest.approx(100.0)
    assert result["South"]["Electronics"] == pytest.approx(1100.0)
    assert result["South"]["Accessories"] == pytest.approx(50.0)


def test_best_selling_product_by_quantity():
    records = sample_records()
    analyzer = SalesDataAnalyzer(records)

    # Laptop: qty 3, Mouse: qty 7 -> Mouse
    assert analyzer.best_selling_product_by_quantity() == "Mouse"


def test_best_selling_product_none_for_empty():
    analyzer = SalesDataAnalyzer([])

    assert analyzer.best_selling_product_by_quantity() is None


def test_average_order_value_empty():
    analyzer = SalesDataAnalyzer([])

    assert analyzer.average_order_value_by_date() == {}


# ---------- Tests for loading CSV ----------

def test_load_sales_reads_valid_rows_and_skips_invalid(tmp_path: Path):
    """
    Create a temporary CSV file with:
    - 2 valid rows
    - 1 malformed row (missing quantity)
    Expect:
      - load_sales returns 2 records
      - values parsed correctly
    """
    csv_file = tmp_path / "sales_data.csv"

    rows = [
        ["order_id", "date", "region", "product", "category", "quantity", "unit_price"],
        ["O-001", "2024-01-01", "North", "Laptop", "Electronics", "2", "1000.0"],
        ["O-002", "2024-01-02", "South", "Mouse", "Accessories", "5", "20.0"],
        # malformed: missing quantity
        ["O-003", "2024-01-03", "West", "Keyboard", "Accessories", "", "45.0"],
    ]

    with csv_file.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    records = load_sales(csv_file)

    first = next(records)
    assert first.order_id == "O-001"
    assert first.date == date(2024, 1, 1)
    assert first.region == "North"
    assert first.product == "Laptop"
    assert first.category == "Electronics"
    assert first.quantity == 2
    assert first.unit_price == pytest.approx(1000.0)
    assert first.line_revenue == pytest.approx(2000.0)
