"""Entry point for the PerformanceAnalyst agent."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys

from .agent import SYSTEM_PROMPT, get_agent_definition  # noqa: F401
from .tools import calculate_affiliate_roi, generate_performance_report

# ---------------------------------------------------------------------------
# Logging — configured from LOG_LEVEL env var so production log aggregators
# can control verbosity without rebuilding the image.
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Security — base directories that data_file and output_dir must reside in.
# Override via DATA_BASE_DIR / OUTPUT_BASE_DIR env vars for deployment.
# ---------------------------------------------------------------------------
_DATA_BASE_DIR = os.path.realpath(
    os.environ.get("DATA_BASE_DIR", os.getcwd())
)
_OUTPUT_BASE_DIR = os.path.realpath(
    os.environ.get("OUTPUT_BASE_DIR", os.getcwd())
)


def _validate_path_within(path: str, base_dir: str, label: str) -> str:
    """Resolve *path* and ensure it is within *base_dir*.

    Returns the resolved absolute path, or raises ValueError on traversal.
    """
    resolved = os.path.realpath(path)
    # Ensure the resolved path starts with the base directory.
    if not resolved.startswith(base_dir + os.sep) and resolved != base_dir:
        raise ValueError(
            f"{label} path '{path}' resolves outside the allowed base "
            f"directory '{base_dir}'"
        )
    return resolved


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
    # ── Path-traversal guards ─────────────────────────────────────────────
    safe_data_file = _validate_path_within(data_file, _DATA_BASE_DIR, "data_file")
    safe_output_dir = _validate_path_within(output_dir, _OUTPUT_BASE_DIR, "output_dir")

    agent_def = get_agent_definition()

    if verbose:
        logger.info("Agent: %s v%s", agent_def["name"], agent_def["version"])
        logger.info("Data file: %s", safe_data_file)
        logger.info("Period: %s", period)
        logger.info("Output dir: %s", safe_output_dir)

    # Validate data file exists
    if not os.path.exists(safe_data_file):
        raise FileNotFoundError(f"Data file not found: {safe_data_file}")

    # Read data file
    with open(safe_data_file, "r") as f:
        raw_data = f.read()

    # Build the analysis prompt — output_dir is NOT interpolated to prevent
    # injection of arbitrary paths into the LLM context.
    prompt = f"""Analyze the following affiliate marketing performance data for the period: {period}

Data file contents:
{raw_data}

Instructions:
1. Use the `generate_performance_report` tool with the data to create a structured report.
2. Use the `calculate_affiliate_roi` tool to compute overall ROI from the totals.
3. Identify the top 3 performing affiliates/campaigns and the bottom 3.
4. Provide at least 5 specific, actionable optimization recommendations.
5. Each recommendation should reference specific data points and include expected outcomes.

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
            logger.warning("Could not auto-extract ROI from data; skipping ROI calculation.")

    # Prepare output
    os.makedirs(safe_output_dir, exist_ok=True)
    output = {
        "agent": agent_def["name"],
        "version": agent_def["version"],
        "data_file": os.path.basename(safe_data_file),
        "period": period,
        "prompt": prompt,
        "report": report,
        "roi": roi_result,
    }

    output_path = os.path.join(safe_output_dir, "performance_report.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    logger.info("Report saved to: %s", output_path)
    return output


def cli() -> None:
    """CLI entry point for the PerformanceAnalyst agent (matches pyproject.toml scripts)."""
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


# Keep `main` as an alias so any external scripts importing it don't break
main = cli

if __name__ == "__main__":
    cli()
