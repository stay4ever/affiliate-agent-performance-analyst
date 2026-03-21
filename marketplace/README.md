# PerformanceAnalyst - Marketplace Listing

## Overview

PerformanceAnalyst is an AI-powered agent that analyzes affiliate marketing performance
data and provides actionable optimization recommendations.

## What It Does

- Parses affiliate performance data (CSV, JSON, or tabular formats)
- Calculates ROI with break-even analysis and monthly projections
- Benchmarks KPIs against industry standards (CTR, conversion rate, EPC)
- Identifies top and bottom performing affiliates and campaigns
- Generates prioritized optimization recommendations backed by data

## Pricing

- **Model:** Per run
- **Estimated cost:** $0.20 - $0.80 per run
- **Billing:** Charged per API usage

## Quick Start

```bash
pip install affiliate-agent-performance-analyst
performance-analyst data.json --period "last 30 days" --verbose
```

## Inputs

| Parameter   | Type   | Required | Default        | Description                          |
|-------------|--------|----------|----------------|--------------------------------------|
| `data_file` | string | Yes      | -              | Path to performance data file        |
| `period`    | string | No       | "last 30 days" | Reporting period description         |

## Outputs

- Performance report with KPI analysis
- ROI calculation with projections
- Ranked optimization recommendations
