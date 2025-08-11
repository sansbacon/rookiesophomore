
# API Reference

## RosterRequirements

Defines the roster requirements for a fantasy football team.

**Constructor:**

```python
RosterRequirements(QB=1, RB=2, WR=2, TE=1, K=0, DST=0, FLEX=1, SUPERFLEX=0, flex_positions=None, superflex_positions=None)
```

**Parameters:**
- `QB`, `RB`, `WR`, `TE`, `K`, `DST`, `FLEX`, `SUPERFLEX`: Number of slots for each position.
- `flex_positions`: List of eligible positions for FLEX (default: ["RB", "WR", "TE"])
- `superflex_positions`: List of eligible positions for SUPERFLEX (default: ["QB", "RB", "WR", "TE"])

## RosterSimulator

Class for generating rosters and running simulations.

**Constructor:**

```python
RosterSimulator(player_pool, requirements, weeks=14, simulations=1000)
```

**Parameters:**
- `player_pool`: pandas DataFrame of player projections
- `requirements`: RosterRequirements object
- `weeks`: Number of weeks in the season
- `simulations`: Number of simulation runs

### Methods

#### filter_players(position)
Returns a DataFrame of players filtered by position.

#### generate_rosters(max_rosters=1000)
Generates up to `max_rosters` random valid rosters as DataFrames.

#### simulate_season(roster_df)
Simulates a season for a given roster DataFrame. Returns a list of total points for each simulation.

#### _simulate_roster(roster_df)
Simulates a single roster and returns a dictionary with roster names, average score, and score distribution.

#### run_simulation(max_rosters=1000, use_multiprocessing=True)
Runs simulations for multiple rosters in parallel. Returns a list of results.

#### plot_top_roster(results, top_n=1)
Plots the score distribution for the top roster(s).

---

See code docstrings for further details and parameter descriptions.
