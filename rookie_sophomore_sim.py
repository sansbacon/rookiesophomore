import numpy as np
import pandas as pd
import itertools
import random
import matplotlib.pyplot as plt

# Sample player pool with mean and std dev for weekly points
player_pool = [
    {"name": "QB1", "position": "QB", "mean": 20, "std": 5},
    {"name": "QB2", "position": "QB", "mean": 18, "std": 6},
    {"name": "RB1", "position": "RB", "mean": 15, "std": 4},
    {"name": "RB2", "position": "RB", "mean": 14, "std": 5},
    {"name": "RB3", "position": "RB", "mean": 13, "std": 6},
    {"name": "WR1", "position": "WR", "mean": 16, "std": 5},
    {"name": "WR2", "position": "WR", "mean": 15, "std": 4},
    {"name": "WR3", "position": "WR", "mean": 14, "std": 6},
    {"name": "TE1", "position": "TE", "mean": 12, "std": 4},
    {"name": "TE2", "position": "TE", "mean": 10, "std": 5},
    {"name": "FLEX1", "position": "RB", "mean": 13, "std": 5},
    {"name": "FLEX2", "position": "WR", "mean": 14, "std": 5}
]

# Positional limits
limits = {
    "QB": 1,
    "RB": 2,
    "WR": 2,
    "TE": 1,
    "FLEX": 1  # FLEX can be RB or WR
}

# Simulation parameters
weeks = 14
simulations = 1000

# Filter players by position
def filter_players(position):
    return [p for p in player_pool if p["position"] == position]

# Generate valid roster combinations
def generate_rosters():
    qbs = filter_players("QB")
    rbs = filter_players("RB")
    wrs = filter_players("WR")
    tes = filter_players("TE")
    flex_pool = [p for p in player_pool if p["position"] in ["RB", "WR"]]

    rosters = []
    for qb in itertools.combinations(qbs, limits["QB"]):
        for rb in itertools.combinations(rbs, limits["RB"]):
            for wr in itertools.combinations(wrs, limits["WR"]):
                for te in itertools.combinations(tes, limits["TE"]):
                    for flex in itertools.combinations(flex_pool, limits["FLEX"]):
                        roster = list(qb + rb + wr + te + flex)
                        # Ensure no duplicate players
                        if len(set(p["name"] for p in roster)) == sum(limits.values()):
                            rosters.append(roster)
    return rosters

# Simulate a season for a given roster
def simulate_season(roster):
    total_points = []
    for _ in range(simulations):
        season_points = 0
        for _ in range(weeks):
            week_points = sum(np.random.normal(p["mean"], p["std"]) for p in roster)
            season_points += week_points
        total_points.append(season_points)
    return total_points

# Run simulation for all rosters
rosters = generate_rosters()
results = []

for roster in rosters:
    scores = simulate_season(roster)
    avg_score = np.mean(scores)
    results.append({
        "roster": [p["name"] for p in roster],
        "average_score": avg_score,
        "score_distribution": scores
    })

# Display top 5 rosters by average score
top_rosters = sorted(results, key=lambda x: x["average_score"], reverse=True)[:5]
for i, r in enumerate(top_rosters, 1):
    print(f"Roster {i}: {r['roster']}")
    print(f"Average Season Score: {r['average_score']:.2f}")
    print()

# Plot distribution for top roster
plt.hist(top_rosters[0]["score_distribution"], bins=30, alpha=0.7)
plt.title("Score Distribution for Top Roster")
plt.xlabel("Season Points")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()
