class RosterRequirements:
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
import itertools
import random
import matplotlib.pyplot as plt

class Player:
    def __init__(self, name, team, position, proj_floor, proj_mean, proj_ceiling, proj_sd):
        self.name = name
        self.team = team
        self.position = position
        self.proj_floor = proj_floor
        self.proj_mean = proj_mean
        self.proj_ceiling = proj_ceiling
        self.proj_sd = proj_sd

class RosterSimulator:
    def __init__(self, player_pool, requirements, weeks=14, simulations=1000):
        self.player_pool = player_pool
        self.requirements = requirements
        self.weeks = weeks
        self.simulations = simulations

    def filter_players(self, position):
        return [p for p in self.player_pool if p.position == position]

    def generate_rosters(self):
        req = self.requirements
        qbs = self.filter_players("QB")
        rbs = self.filter_players("RB")
        wrs = self.filter_players("WR")
        tes = self.filter_players("TE")
        ks = self.filter_players("K")
        dsts = self.filter_players("DST")
        flex_pool = [p for p in self.player_pool if p.position in req.flex_positions]
        superflex_pool = [p for p in self.player_pool if p.position in req.superflex_positions]
        rosters = []
        for qb in itertools.combinations(qbs, req.QB):
            for rb in itertools.combinations(rbs, req.RB):
                for wr in itertools.combinations(wrs, req.WR):
                    for te in itertools.combinations(tes, req.TE):
                        for k in itertools.combinations(ks, req.K):
                            for dst in itertools.combinations(dsts, req.DST):
                                for flex in itertools.combinations(flex_pool, req.FLEX):
                                    for superflex in itertools.combinations(superflex_pool, req.SUPERFLEX):
                                        roster = list(qb + rb + wr + te + k + dst + flex + superflex)
                                        # Ensure no duplicate players
                                        total_slots = req.QB + req.RB + req.WR + req.TE + req.K + req.DST + req.FLEX + req.SUPERFLEX
                                        if len(set(p.name for p in roster)) == total_slots:
                                            rosters.append(roster)
        return rosters

    def simulate_season(self, roster):
        total_points = []
        for _ in range(self.simulations):
            season_points = 0
            for _ in range(self.weeks):
                week_points = sum(np.random.normal(p.mean, p.std) for p in roster)
                season_points += week_points
            total_points.append(season_points)
        return total_points

    def run_simulation(self):
        rosters = self.generate_rosters()
        results = []
        for roster in rosters:
            scores = self.simulate_season(roster)
            avg_score = np.mean(scores)
            results.append({
                "roster": [p.name for p in roster],
                "average_score": avg_score,
                "score_distribution": scores
            })
        return results

    def plot_top_roster(self, results, top_n=1):
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
