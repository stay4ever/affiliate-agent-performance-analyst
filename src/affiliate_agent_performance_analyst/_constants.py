"""
_constants.py
~~~~~~~~~~~~~
Standalone constants module — imported by agent.py, __init__.py, and entry.py.

Kept in its own file to break the circular import chain:
  __init__.py → entry.py → agent.py → __init__.py  ☠️
becomes:
  __init__.py → _constants.py  ✅
  agent.py    → _constants.py  ✅
  entry.py    → agent.py       ✅
"""

AGENT_NAME: str = "PerformanceAnalyst"
AGENT_DESCRIPTION: str = (
    "AI-powered affiliate marketing performance analyst that calculates ROI, "
    "benchmarks KPIs, and generates actionable optimisation reports."
)
__version__: str = "0.1.0"
