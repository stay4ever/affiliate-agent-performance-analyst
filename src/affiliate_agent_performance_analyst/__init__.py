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

from affiliate_agent_performance_analyst.entry import run_performance_analyst  # noqa: F401

__all__ = ["run_performance_analyst"]
__version__ = "0.1.0"
