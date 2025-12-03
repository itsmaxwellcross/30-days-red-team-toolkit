# DGA Framework

Domain Generation Algorithm (DGA) Framework for C2 operations.

## Installation

```bash
# Method 1: Use directly
cd dga/
python -m run --help

# Method 2: Install as package
pip install -e .
dga --help
```

## Usage Examples

### Generate Domains

```bash
# Generate 10 domains for today
python -m dga.run --generate 10

# Generate domains for next 7 days (20 per day)
python -m dga.run --daily 7 --per-day 20

# Generate time-based domain (changes hourly)
python -m dga.run --time-based

# Use custom TLD
python -m dga.run --daily 7 --tld .net
```

### Check Domain Availability

```bash
# Generate and check domains
python -m dga.run --daily 7 --check-domains

# Adjust timeout
python -m dga.run --daily 7 --check-domains --timeout 5
```

### Export Domains

```bash
# Save as JSON
python -m dga.run --daily 7 --output domains.json --format json

# Save as CSV
python -m dga.run --daily 7 --output domains.csv --format csv

# Save as text
python -m dga.run --daily 7 --output domains.txt
```

### Registration & Cost

```bash
# Generate registration commands
python -m dga.run --daily 7 --registration-commands --registrar namecheap

# Estimate cost
python -m dga.run --daily 7 --per-day 20 --cost-estimate --price-per-domain 12
```

### Agent Mode

```bash
# Run agent that finds active DGA domains
python -m dga.run --agent-mode

# Custom beacon interval
python -m dga.run --agent-mode --beacon-interval 600 --jitter 120
```

## Module Structure

```
dga/
├── __init__.py       # Package initialization
├── generator.py      # Core DGA generation logic
├── agent.py          # Agent-side implementation
├── utils.py          # Helper functions
└── run.py            # CLI interface
```

## Programmatic Usage

```python
from dga import DGAGenerator, DGAAgent

# Generate domains
dga = DGAGenerator(tld='.com')
domains = dga.generate_daily_domains(num_days=7, domains_per_day=10)

# Use in agent
agent = DGAAgent(dga)
active_domain = agent.beacon_with_dga()
```