"""
affiliate_agent_performance_analyst
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
AI-powered affiliate marketing performance analysis package.

Public API
----------
>>> from affiliate_agent_performance_analyst import run_performance_analyst
>>> from affiliate_agent_performance_analyst.tools import (
...     generate_performance_report,
...     calculate_affiliate_roi,
... )
"""

from __future__ import annotations

# Load .env before any other imports so env vars are available everywhere
from dotenv import load_dotenv

load_dotenv()

from affiliate_agent_performance_analyst.entry import run_performance_analyst  # noqa: F401, E402

# Agent identity constants — consumed by agent.py and any external integrations
AGENT_NAME: str = "PerformanceAnalyst"
AGENT_DESCRIPTION: str = (
    "AI-powered affiliate marketing performance analyst that calculates ROI, "
    "benchmarks KPIs, and generates actionable optimisation reports."
)

__all__ = [
    "run_performance_analyst",
    "AGENT_NAME",
    "AGENT_DESCRIPTION",
]
__version__ = "0.1.0"
