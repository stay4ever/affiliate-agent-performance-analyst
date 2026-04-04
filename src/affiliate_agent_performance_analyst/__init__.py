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

# Constants live in _constants.py to break the circular import:
#   __init__ -> entry -> agent -> __init__  (was circular)
#   __init__ -> _constants                  (safe)
from affiliate_agent_performance_analyst._constants import (  # noqa: E402
    AGENT_NAME,
    AGENT_DESCRIPTION,
    __version__,
)

# Lazy public API — imported here for convenience but NOT at module load time
# to avoid triggering the full import chain during `pip install` / CLI startup.
def __getattr__(name: str):
    if name == "run_performance_analyst":
        from affiliate_agent_performance_analyst.entry import run_performance_analyst
        return run_performance_analyst
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "run_performance_analyst",
    "AGENT_NAME",
    "AGENT_DESCRIPTION",
    "__version__",
]
