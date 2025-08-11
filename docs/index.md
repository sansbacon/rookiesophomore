
# Rookiesophomore Documentation

Welcome to the documentation for the Rookiesophomore fantasy football simulation library.

## Overview
Rookiesophomore is a Python library for projecting, ranking, and simulating fantasy football players and leagues. It is designed for speed, flexibility, and extensibility, supporting custom roster requirements and large-scale simulations.

## Features
- Project, rank, and simulate fantasy football players and leagues
- Fast, vectorized simulation engine using pandas and NumPy
- Flexible roster requirements (including FLEX and SUPERFLEX)
- Command-line interface (CLI) for ranking and simulation
- Extensible for custom scoring, projections, and league formats

## Installation

```bash
pip install rookiesophomore
```

Or clone the repository and install dependencies:

```bash
git clone https://github.com/sansbacon/rookiesophomore.git
cd rookiesophomore
pip install -e .
```

## Quickstart

### Simulate a League

```python
from rookiesophomore.simulation import RosterSimulator, RosterRequirements
import pandas as pd

# Load player pool from CSV
player_pool = pd.read_csv('player_pool.csv')
requirements = RosterRequirements(QB=1, RB=2, WR=2, TE=1, FLEX=1)
sim = RosterSimulator(player_pool, requirements, weeks=14, simulations=10000)
results = sim.run_simulation(max_rosters=500)
```

### Command Line Usage

```bash
rookiesophomore rank --datafile player_pool.csv --out-csv roster.csv
rookiesophomore simulate --player-pool-file player_pool.csv --roster-type standard --weeks 14 --simulations 10000 --top-n 5
```

## Documentation Structure
- [API Reference](api.md): Detailed API documentation
- [Examples](examples.md): Usage examples and CLI walkthroughs
- [FAQ](faq.md): Frequently asked questions

## Contributing
See [CONTRIBUTING.md](https://github.com/sansbacon/rookiesophomore/blob/main/CONTRIBUTING.md) for guidelines.

## License
MIT License
