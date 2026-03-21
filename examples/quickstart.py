"""Quickstart example for the PerformanceAnalyst agent."""

import asyncio
import json
import os
import tempfile

from affiliate_agent_performance_analyst.entry import run_performance_analyst


# Sample affiliate performance data
SAMPLE_DATA = [
    {
        "affiliate_name": "TechReviews Pro",
        "clicks": 15000,
        "impressions": 500000,
        "conversions": 450,
        "revenue": 22500.00,
        "cost": 6000.00,
        "channel": "blog",
    },
    {
        "affiliate_name": "DealHunter Daily",
        "clicks": 8000,
        "impressions": 200000,
        "conversions": 120,
        "revenue": 4800.00,
        "cost": 3500.00,
        "channel": "email",
    },
    {
        "affiliate_name": "Social Buzz Network",
        "clicks": 25000,
        "impressions": 1000000,
        "conversions": 200,
        "revenue": 8000.00,
        "cost": 7500.00,
        "channel": "social_media",
    },
    {
        "affiliate_name": "CouponKing",
        "clicks": 12000,
        "impressions": 300000,
        "conversions": 600,
        "revenue": 18000.00,
        "cost": 4000.00,
        "channel": "coupon_site",
    },
    {
        "affiliate_name": "NicheBlogger",
        "clicks": 3000,
        "impressions": 50000,
        "conversions": 150,
        "revenue": 9000.00,
        "cost": 1500.00,
        "channel": "blog",
    },
]


async def main():
    """Run the quickstart example."""
    # Write sample data to a temp file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        json.dump(SAMPLE_DATA, f, indent=2)
        data_file = f.name

    try:
        result = await run_performance_analyst(
            data_file=data_file,
            period="last 30 days",
            output_dir="./output",
            verbose=True,
        )

        print("\n--- ROI Summary ---")
        if result.get("roi"):
            roi = result["roi"]
            print(f"Total Revenue: ${roi['total_revenue']:,.2f}")
            print(f"Total Cost:    ${roi['total_cost']:,.2f}")
            print(f"Profit:        ${roi['profit']:,.2f}")
            print(f"ROI:           {roi['roi_percentage']:.1f}%")
            print(f"Assessment:    {roi['assessment']}")
            print(f"Monthly Projected Revenue: ${roi['monthly_projected_revenue']:,.2f}")
        else:
            print("ROI calculation was not available.")

    finally:
        os.unlink(data_file)


if __name__ == "__main__":
    asyncio.run(main())
