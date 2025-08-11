# Examples

## Simulating a League

```python
import pandas as pd
from rookiesophomore.simulation import RosterSimulator, RosterRequirements

player_pool = pd.read_csv('player_pool.csv')
requirements = RosterRequirements(QB=1, RB=2, WR=2, TE=1, FLEX=1)
sim = RosterSimulator(player_pool, requirements, weeks=14, simulations=10000)
results = sim.run_simulation(max_rosters=500)
for r in results[:3]:
    print(r['roster'], r['average_score'])
```

## CLI Usage

```bash
rookiesophomore rank --datafile player_pool.csv --out-csv roster.csv
rookiesophomore simulate --player-pool-file player_pool.csv --roster-type standard --weeks 14 --simulations 10000 --top-n 5
```

## Custom Roster Requirements

```python
requirements = RosterRequirements(QB=1, RB=2, WR=3, TE=1, FLEX=2, SUPERFLEX=1, flex_positions=["RB", "WR", "TE"], superflex_positions=["QB", "RB", "WR", "TE"])
```

## Saving Results

```python
import pandas as pd
results_df = pd.DataFrame(results)
results_df.to_csv('simulation_results.csv', index=False)
```
