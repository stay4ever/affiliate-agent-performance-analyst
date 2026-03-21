"""Entry point for the PerformanceAnalyst agent."""

import asyncio
import json
import os
import sys

from .agent import SYSTEM_PROMPT, get_agent_definition
from .tools import calculate_affiliate_roi, generate_performance_report


async def run_performance_analyst(
    data_file: str,
    period: str = "last 30 days",
    output_dir: str = "./output",
    model: str | None = None,
    max_budget_usd: float | None = None,
    verbose: bool = False,
) -> dict:
    """Run the PerformanceAnalyst agent on a data file.

    Args:
        data_file: Path to the performance data file (CSV, JSON).
        period: The reporting period description.
        output_dir: Directory to save the output report.
        model: Optional model override for the agent.
        max_budget_usd: Optional maximum budget in USD for the run.
        verbose: Whether to print verbose output.

    Returns:
        A dictionary containing the analysis results.
    """
    agent_def = get_agent_definition()

    if verbose:
        print(f"Agent: {agent_def['name']} v{agent_def['version']}")
        print(f"Data file: {data_file}")
        print(f"Period: {period}")
        print(f"Output dir: {output_dir}")

    # Validate data file exists
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")

    # Read data file
    with open(data_file, "r") as f:
        raw_data = f.read()

    # Build the analysis prompt
    prompt = f"""Analyze the following affiliate marketing performance data for the period: {period}

Data file contents:
{raw_data}

Instructions:
1. Use the `generate_performance_report` tool with the data to create a structured report.
2. Use the `calculate_affiliate_roi` tool to compute overall ROI from the totals.
3. Identify the top 3 performing affiliates/campaigns and the bottom 3.
4. Provide at least 5 specific, actionable optimization recommendations.
5. Each recommendation should reference specific data points and include expected outcomes.
6. Save the complete report to {output_dir}/performance_report.json

Focus on:
- Which affiliates/campaigns are driving the most value?
- Where is money being wasted?
- What quick wins could improve performance in the next 30 days?
- What strategic changes could improve performance over the next quarter?
"""

    # Generate the performance report
    report = generate_performance_report(raw_data, period)

    # Attempt to extract totals for ROI calculation
    roi_result = None
    try:
        metrics = json.loads(raw_data)
        if isinstance(metrics, dict):
            metrics = [metrics]
        if isinstance(metrics, list) and len(metrics) > 0:
            total_cost = sum(float(m.get("cost", 0)) for m in metrics)
            total_revenue = sum(float(m.get("revenue", 0)) for m in metrics)
            roi_result = calculate_affiliate_roi(
                total_cost=total_cost,
                total_revenue=total_revenue,
                time_period_days=30,
            )
    except (json.JSONDecodeError, TypeError, ValueError):
        if verbose:
            print("Could not auto-extract ROI from data; skipping ROI calculation.")

    # Prepare output
    os.makedirs(output_dir, exist_ok=True)
    output = {
        "agent": agent_def["name"],
        "version": agent_def["version"],
        "data_file": data_file,
        "period": period,
        "prompt": prompt,
        "report": report,
        "roi": roi_result,
    }

    output_path = os.path.join(output_dir, "performance_report.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    if verbose:
        print(f"Report saved to: {output_path}")

    return output


def main():
    """CLI entry point for the PerformanceAnalyst agent."""
    if len(sys.argv) < 2:
        print("Usage: performance-analyst <data_file> [--period PERIOD] [--verbose]")
        print()
        print("Arguments:")
        print("  data_file        Path to performance data file (CSV, JSON)")
        print("  --period PERIOD  Reporting period (default: 'last 30 days')")
        print("  --verbose        Enable verbose output")
        sys.exit(1)

    data_file = sys.argv[1]
    period = "last 30 days"
    verbose = False

    # Parse optional arguments
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--period" and i + 1 < len(args):
            period = args[i + 1]
            i += 2
        elif args[i] == "--verbose":
            verbose = True
            i += 1
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    result = asyncio.run(
        run_performance_analyst(
            data_file=data_file,
            period=period,
            verbose=verbose,
        )
    )

    if not verbose:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
