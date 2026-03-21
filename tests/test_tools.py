"""Tests for PerformanceAnalyst tools."""

import json
import pytest

from affiliate_agent_performance_analyst.tools import (
    calculate_affiliate_roi,
    generate_performance_report,
)


class TestGeneratePerformanceReport:
    """Tests for generate_performance_report."""

    def test_valid_json_list(self):
        metrics = json.dumps([
            {"affiliate": "A", "clicks": 100, "revenue": 500},
            {"affiliate": "B", "clicks": 200, "revenue": 1200},
        ])
        result = generate_performance_report(metrics, "last 30 days")

        assert "error" not in result
        assert result["period"] == "last 30 days"
        assert result["report_date"]  # non-empty
        assert len(result["metrics"]) == 2
        assert "analysis_framework" in result
        assert "kpis" in result["analysis_framework"]
        assert "benchmarks" in result["analysis_framework"]
        assert result["analysis_framework"]["benchmarks"]["good_ctr"] == "2-5%"
        assert result["analysis_framework"]["benchmarks"]["good_conversion_rate"] == "1-3%"
        assert result["analysis_framework"]["benchmarks"]["good_epc"] == "$0.50-$2.00"
        assert "optimization_areas" in result
        assert "instructions" in result

    def test_valid_json_single_object(self):
        metrics = json.dumps({"affiliate": "A", "clicks": 100})
        result = generate_performance_report(metrics, "Q1 2025")

        assert "error" not in result
        assert len(result["metrics"]) == 1
        assert result["period"] == "Q1 2025"

    def test_invalid_json(self):
        result = generate_performance_report("not valid json{", "last 7 days")

        assert "error" in result
        assert "Invalid JSON" in result["error"]
        assert "hint" in result

    def test_wrong_type_input(self):
        result = generate_performance_report(12345, "last 7 days")

        assert "error" in result

    def test_non_object_non_list_json(self):
        result = generate_performance_report('"just a string"', "last 7 days")

        assert "error" in result

    def test_empty_list(self):
        result = generate_performance_report("[]", "last 30 days")

        assert "error" not in result
        assert result["metrics"] == []

    def test_kpis_present(self):
        result = generate_performance_report('[{"clicks": 10}]', "test")
        kpis = result["analysis_framework"]["kpis"]

        assert "CTR (Click-Through Rate)" in kpis
        assert "Conversion Rate" in kpis
        assert "EPC (Earnings Per Click)" in kpis
        assert "RPM (Revenue Per Mille)" in kpis
        assert "AOV (Average Order Value)" in kpis
        assert "ROI (Return on Investment)" in kpis


class TestCalculateAffiliateROI:
    """Tests for calculate_affiliate_roi."""

    def test_profitable_campaign(self):
        result = calculate_affiliate_roi(
            total_cost=5000.0,
            total_revenue=12000.0,
            time_period_days=30,
        )

        assert result["profit"] == 7000.0
        assert result["roi_percentage"] == 140.0
        assert result["assessment"] == "profitable"
        assert result["daily_revenue"] == 400.0
        assert result["daily_profit"] == pytest.approx(233.33, abs=0.01)
        assert result["monthly_projected_revenue"] == 12000.0
        assert result["break_even_days"] is not None

    def test_unprofitable_campaign(self):
        result = calculate_affiliate_roi(
            total_cost=10000.0,
            total_revenue=4000.0,
            time_period_days=30,
        )

        assert result["profit"] == -6000.0
        assert result["roi_percentage"] == -60.0
        assert result["assessment"] == "unprofitable"
        assert result["break_even_days"] is None

    def test_break_even_campaign(self):
        result = calculate_affiliate_roi(
            total_cost=5000.0,
            total_revenue=5000.0,
            time_period_days=30,
        )

        assert result["profit"] == 0.0
        assert result["roi_percentage"] == 0.0
        assert result["assessment"] == "break-even"

    def test_zero_revenue(self):
        result = calculate_affiliate_roi(
            total_cost=5000.0,
            total_revenue=0.0,
            time_period_days=30,
        )

        assert result["assessment"] == "unprofitable"
        assert result["break_even_days"] is None

    def test_zero_cost(self):
        result = calculate_affiliate_roi(
            total_cost=0.0,
            total_revenue=1000.0,
            time_period_days=10,
        )

        assert result["profit"] == 1000.0
        assert result["roi_percentage"] == 0.0  # division by zero handled
        assert result["assessment"] == "profitable"

    def test_invalid_time_period(self):
        result = calculate_affiliate_roi(
            total_cost=1000.0,
            total_revenue=2000.0,
            time_period_days=0,
        )

        assert "error" in result

    def test_negative_time_period(self):
        result = calculate_affiliate_roi(
            total_cost=1000.0,
            total_revenue=2000.0,
            time_period_days=-5,
        )

        assert "error" in result

    def test_monthly_projections(self):
        result = calculate_affiliate_roi(
            total_cost=3000.0,
            total_revenue=9000.0,
            time_period_days=15,
        )

        assert result["daily_revenue"] == 600.0
        assert result["monthly_projected_revenue"] == 18000.0
        assert result["daily_profit"] == 400.0
        assert result["monthly_projected_profit"] == 12000.0
