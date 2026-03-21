# PerformanceAnalyst

AI-powered affiliate marketing performance analysis agent.

## Installation

```bash
pip install affiliate-agent-performance-analyst
```

## Usage

### CLI

```bash
performance-analyst data.json --period "last 30 days" --verbose
```

### Python API

```python
import asyncio
from affiliate_agent_performance_analyst.entry import run_performance_analyst

result = asyncio.run(run_performance_analyst(
    data_file="data.json",
    period="last 30 days",
    verbose=True,
))
```

### Tools

```python
from affiliate_agent_performance_analyst.tools import (
    generate_performance_report,
    calculate_affiliate_roi,
)

# Generate a performance report
report = generate_performance_report(
    metrics_json='[{"clicks": 1000, "conversions": 50, "revenue": 2500, "cost": 800}]',
    period="last 30 days",
)

# Calculate ROI
roi = calculate_affiliate_roi(
    total_cost=5000.0,
    total_revenue=12000.0,
    time_period_days=30,
)
```

## Features

- Performance data analysis (CSV, JSON, or any tabular format)
- ROI calculation with break-even analysis
- KPI benchmarking (CTR, conversion rate, EPC, RPM, AOV)
- Top/bottom performer identification
- Revenue forecasting
- Actionable optimization recommendations

## License

MIT
