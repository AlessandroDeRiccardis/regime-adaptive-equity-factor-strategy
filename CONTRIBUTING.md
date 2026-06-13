# Contributing

Contributions should preserve the repository's core research principles:
point-in-time signal construction, explicit benchmark definitions, reproducible
configuration, and transparent limitations.

## Development Workflow

```bash
python -m pip install -e ".[dev]"
make lint
make test
make reproduce
```

Before opening a pull request:

1. Add focused synthetic tests for changed research or accounting behavior.
2. Keep proprietary or licensed data outside Git.
3. Document any change to signal timing, benchmark construction, transaction
   costs, or performance definitions.
4. Do not describe backtested performance as evidence of live profitability.

Generated outputs under `data/processed/`, `reports/figures/`, and
`reports/tables/` are intentionally ignored.
