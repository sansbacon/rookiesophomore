# FAQ

## What formats are supported for player pools?

You can use CSV or JSON files. The recommended format is CSV with columns: `name`, `team`, `position`, `proj_floor`, `proj_mean`, `proj_ceiling`, `proj_sd`.

## How do I customize roster requirements?

Use the `RosterRequirements` class to set the number of slots and eligible positions for FLEX and SUPERFLEX.

## How do I run large simulations efficiently?

Rookiesophomore uses vectorized NumPy and pandas operations, and multiprocessing for parallel simulation. You can control the number of rosters and simulations for performance.

## Can I use the library for other sports?

The core simulation engine is flexible and can be adapted for other sports with similar roster and scoring structures.

## How do I contribute?

See the [CONTRIBUTING.md](https://github.com/sansbacon/rookiesophomore/blob/main/CONTRIBUTING.md) for guidelines.
