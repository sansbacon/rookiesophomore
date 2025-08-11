
import typer
from rookiesophomore.ranking import build_roster
from rookiesophomore.simulation import RosterSimulator, Player, RosterRequirements
import pandas as pd
import json

app = typer.Typer()

# Predefined roster types
ROSTER_PRESETS = {
    "standard": {"QB": 1, "RB": 2, "WR": 2, "TE": 1, "FLEX": 1},
    "superflex": {"QB": 1, "RB": 2, "WR": 2, "TE": 1, "SUPERFLEX": 1},
    "ppr": {"QB": 1, "RB": 2, "WR": 3, "TE": 1, "FLEX": 1},
}

def load_player_pool(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        return [Player(row["name"], row.get("team", ""), row["position"], row["proj_floor"], row["proj_mean"], row["proj_ceiling"], row["proj_sd"]) for _, row in df.iterrows()]
    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            data = json.load(f)
        return [Player(p["name"], p.get("team", ""), p["position"], p["proj_floor"], p["proj_mean"], p["proj_ceiling"], p["proj_sd"]) for p in data]
    else:
        raise ValueError("Unsupported player pool file format. Use CSV or JSON.")

@app.command()
def rank(
    datafile: str,
    out_csv: str = "roster.csv",
    risk_aversion: float = 1.0
):
    """Rank rookie and sophomore players from a CSV file."""
    roster = build_roster(datafile, lambda_risk=risk_aversion)
    roster.to_csv(out_csv, index=False)
    typer.echo(f"Roster saved to {out_csv}")


@app.command()
def simulate(
    player_pool_file: str = typer.Option(None, help="CSV or JSON file with player pool"),
    roster_type: str = typer.Option("standard", help="Predefined roster type (standard, superflex, ppr)"),
    qb: int = typer.Option(None, help="Number of QBs"),
    rb: int = typer.Option(None, help="Number of RBs"),
    wr: int = typer.Option(None, help="Number of WRs"),
    te: int = typer.Option(None, help="Number of TEs"),
    flex: int = typer.Option(None, help="Number of FLEX spots"),
    superflex: int = typer.Option(None, help="Number of SUPERFLEX spots"),
    weeks: int = typer.Option(14, help="Number of weeks in the season"),
    simulations: int = typer.Option(1000, help="Number of simulation runs"),
    top_n: int = typer.Option(1, help="Number of top rosters to display"),
    save_plot: str = typer.Option(None, help="Filename to save the plot (optional)")
):
    """Run a roster simulation with configurable player pool and roster limits."""
    # Load player pool
    if player_pool_file:
        player_pool = load_player_pool(player_pool_file)
    else:
        # Demo pool
        player_pool = [
            Player("QB1", "TeamA", "QB", 10, 20, 30, 5),
            Player("QB2", "TeamB", "QB", 8, 18, 28, 6),
            Player("RB1", "TeamC", "RB", 7, 15, 23, 4),
            Player("RB2", "TeamD", "RB", 6, 14, 22, 5),
            Player("RB3", "TeamE", "RB", 5, 13, 21, 6),
            Player("WR1", "TeamF", "WR", 8, 16, 24, 5),
            Player("WR2", "TeamG", "WR", 7, 15, 23, 4),
            Player("WR3", "TeamH", "WR", 6, 14, 22, 6),
            Player("TE1", "TeamI", "TE", 6, 12, 18, 4),
            Player("TE2", "TeamJ", "TE", 5, 10, 15, 5),
            Player("FLEX1", "TeamK", "RB", 6, 13, 20, 5),
            Player("FLEX2", "TeamL", "WR", 7, 14, 21, 5)
        ]
    # Build RosterRequirements
    preset = ROSTER_PRESETS.get(roster_type, ROSTER_PRESETS["standard"])
    req = RosterRequirements(
        QB=qb if qb is not None else preset.get("QB", 0),
        RB=rb if rb is not None else preset.get("RB", 0),
        WR=wr if wr is not None else preset.get("WR", 0),
        TE=te if te is not None else preset.get("TE", 0),
        FLEX=flex if flex is not None else preset.get("FLEX", 0),
        SUPERFLEX=superflex if superflex is not None else preset.get("SUPERFLEX", 0)
    )

    sim = RosterSimulator(player_pool, req, weeks=weeks, simulations=simulations)
    results = sim.run_simulation()
    top_rosters = sorted(results, key=lambda x: x["average_score"], reverse=True)[:top_n]
    for i, r in enumerate(top_rosters, 1):
        typer.echo(f"Roster {i}: {r['roster']}")
        typer.echo(f"Average Season Score: {r['average_score']:.2f}")
        typer.echo(f"Min: {min(r['score_distribution']):.2f}  Max: {max(r['score_distribution']):.2f}")
        typer.echo("")
    if save_plot:
        import matplotlib.pyplot as plt
        plt.hist(top_rosters[0]["score_distribution"], bins=30, alpha=0.7)
        plt.title("Score Distribution for Top Roster")
        plt.xlabel("Season Points")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.savefig(save_plot)
        typer.echo(f"Plot saved to {save_plot}")

if __name__ == "__main__":
    app()
