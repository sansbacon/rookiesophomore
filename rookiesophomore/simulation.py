class RosterRequirements:
    """
    Defines the roster requirements for a fantasy football team.

    Args:
        QB (int): Number of quarterbacks.
        RB (int): Number of running backs.
        WR (int): Number of wide receivers.
        TE (int): Number of tight ends.
        K (int): Number of kickers.
        DST (int): Number of defenses/special teams.
        FLEX (int): Number of flex spots.
        SUPERFLEX (int): Number of superflex spots.
        flex_positions (List[str], optional): Eligible positions for flex.
        superflex_positions (List[str], optional): Eligible positions for superflex.
    """
    def __init__(
        self,
        QB=1, RB=2, WR=2, TE=1, K=0, DST=0, FLEX=1, SUPERFLEX=0,
        flex_positions=None, superflex_positions=None
    ):
        self.QB = QB
        self.RB = RB
        self.WR = WR
        self.TE = TE
        self.K = K
        self.DST = DST
        self.FLEX = FLEX
        self.SUPERFLEX = SUPERFLEX
        self.flex_positions = flex_positions or ["RB", "WR", "TE"]
        self.superflex_positions = superflex_positions or ["QB", "RB", "WR", "TE"]

"""
Simulation module for fantasy football rosters.
"""
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt



class RosterSimulator:
    def __init__(self, player_pool, requirements, weeks=14, simulations=1000):
        """
        Initialize the RosterSimulator.

        Args:
            player_pool (pd.DataFrame or list): Player pool as DataFrame or list of dicts.
            requirements (RosterRequirements): Roster requirements.
            weeks (int): Number of weeks in the season.
            simulations (int): Number of simulation runs.
        """
        self.player_pool = player_pool
        self.requirements = requirements
        self.weeks = weeks
        self.simulations = simulations

    def filter_players(self, position):
        """
        Filter players by position.

        Args:
            position (str): Position to filter by.

        Returns:
            pd.DataFrame: Filtered DataFrame of players.
        """
        df = self.player_pool if isinstance(self.player_pool, pd.DataFrame) else pd.DataFrame([vars(p) for p in self.player_pool])
        return df[df['position'] == position]

    def generate_rosters(self, max_rosters=1000):
        """
        Generate random valid rosters using vectorized sampling.

        Args:
            max_rosters (int): Maximum number of rosters to sample.

        Returns:
            List[pd.DataFrame]: List of DataFrames, each representing a roster.
        """
        import numpy as np
        import pandas as pd
        req = self.requirements
        df = self.player_pool if isinstance(self.player_pool, pd.DataFrame) else pd.DataFrame([vars(p) for p in self.player_pool])
        pos_groups = [
            (df.index[df['position'] == 'QB'].to_numpy(), req.QB),
            (df.index[df['position'] == 'RB'].to_numpy(), req.RB),
            (df.index[df['position'] == 'WR'].to_numpy(), req.WR),
            (df.index[df['position'] == 'TE'].to_numpy(), req.TE),
            (df.index[df['position'] == 'K'].to_numpy(), req.K),
            (df.index[df['position'] == 'DST'].to_numpy(), req.DST),
            (df.index[df['position'].isin(req.flex_positions)].to_numpy(), req.FLEX),
            (df.index[df['position'].isin(req.superflex_positions)].to_numpy(), req.SUPERFLEX)
        ]
        roster_matrix = []
        for idx, count in pos_groups:
            if count > 0:
                samples = np.array([np.random.choice(idx, min(count, len(idx)), replace=False) for _ in range(max_rosters)])
                roster_matrix.append(samples)
        if roster_matrix:
            roster_matrix = np.concatenate(roster_matrix, axis=1)
        else:
            roster_matrix = np.empty((max_rosters, 0), dtype=int)
        unique_mask = np.array([len(np.unique(row)) == row.size for row in roster_matrix])
        unique_rosters = roster_matrix[unique_mask]
        # Return list of DataFrames, each representing a roster
        return [df.loc[list(roster)].reset_index(drop=True) for roster in unique_rosters]

    def simulate_season(self, roster_df):
        """
        Simulate a fantasy football season for a given roster.

        Args:
            roster_df (pd.DataFrame): DataFrame of player projections.

        Returns:
            List[float]: Total points for each simulation.
        """
        means = roster_df['proj_mean'].to_numpy()
        sds = roster_df['proj_sd'].to_numpy()
        scores = np.random.normal(
            loc=means[None, None, :],
            scale=sds[None, None, :],
            size=(self.simulations, self.weeks, len(means))
        )
        season_points = scores.sum(axis=2).sum(axis=1)
        return season_points.tolist()

    def _simulate_roster(self, roster_df):
        """
        Simulate a single roster and return summary statistics.

        Args:
            roster_df (pd.DataFrame): DataFrame of player projections.

        Returns:
            dict: Roster names, average score, and score distribution.
        """
        scores = self.simulate_season(roster_df)
        avg_score = np.mean(scores)
        return {
            "roster": roster_df['name'].tolist(),
            "average_score": avg_score,
            "score_distribution": scores
        }

    def run_simulation(self, max_rosters=1000, use_multiprocessing=True):
        """
        Run simulations for multiple rosters in parallel.

        Args:
            max_rosters (int): Maximum number of rosters to sample.
            use_multiprocessing (bool): Whether to use multiprocessing.

        Returns:
            List[dict]: Simulation results for each roster.
        """
        import multiprocessing as mp
        rosters = self.generate_rosters(max_rosters=max_rosters)
        if use_multiprocessing and len(rosters) > 1:
            with mp.Pool() as pool:
                results = pool.map(self._simulate_roster, rosters)
        else:
            results = [self._simulate_roster(roster) for roster in rosters]
        return results

    def plot_top_roster(self, results, top_n=1):
        """
        Plot the score distribution for the top roster(s).

        Args:
            results (List[dict]): Simulation results.
            top_n (int): Number of top rosters to plot.
        """
        top_rosters = sorted(results, key=lambda x: x["average_score"], reverse=True)[:top_n]
        for i, r in enumerate(top_rosters, 1):
            print(f"Roster {i}: {r['roster']}")
            print(f"Average Season Score: {r['average_score']:.2f}\n")
        plt.hist(top_rosters[0]["score_distribution"], bins=30, alpha=0.7)
        plt.title("Score Distribution for Top Roster")
        plt.xlabel("Season Points")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()
