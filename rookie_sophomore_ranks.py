import pandas as pd
import numpy as np

# -------------------- Constants --------------------
POSITION_LIMITS = {
    'QB': 1,
    'RB': 2,
    'WR': 3,
    'TE': 1,
    'SUPERFLEX': 1  # Can be QB, RB, WR, or TE
}
BENCH_SIZE = 6
RISK_AVERSION = 1.0

# -------------------- Functions --------------------

def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

def filter_eligible_players(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['experience'].isin(['rookie', 'sophomore'])].copy()

def calculate_risk_adjusted_score(df: pd.DataFrame, lambda_risk: float) -> pd.DataFrame:
    df['std_dev'] = (df['ceiling_projection'] - df['floor_projection']) / 4
    df['risk_adjusted_score'] = df['mean_projection'] - lambda_risk * df['std_dev']
    return df.sort_values(by='risk_adjusted_score', ascending=False)

def select_starters(df: pd.DataFrame, limits: dict) -> pd.DataFrame:
    selected = []
    for pos in ['QB', 'RB', 'WR', 'TE']:
        top_pos = df[df['position'] == pos].head(limits[pos])
        selected.append(top_pos)
    remaining = df[~df.index.isin(pd.concat(selected).index)]
    superflex_pool = remaining[remaining['position'].isin(['QB', 'RB', 'WR', 'TE'])]
    superflex_pick = superflex_pool.head(limits['SUPERFLEX'])
    selected.append(superflex_pick)
    return pd.concat(selected)

def select_bench(df: pd.DataFrame, starters: pd.DataFrame, bench_size: int) -> pd.DataFrame:
    remaining = df[~df.index.isin(starters.index)]
    return remaining.head(bench_size)

def build_roster(filepath: str,
                 position_limits: dict = POSITION_LIMITS,
                 bench_size: int = BENCH_SIZE,
                 lambda_risk: float = RISK_AVERSION) -> pd.DataFrame:
    
    df = load_data(filepath)
    eligible = filter_eligible_players(df)
    scored = calculate_risk_adjusted_score(eligible, lambda_risk)
    starters = select_starters(scored, position_limits)
    bench = select_bench(scored, starters, bench_size)
    
    roster = pd.concat([starters, bench])
    roster['role'] = ['starter'] * len(starters) + ['bench'] * len(bench)
    roster['final_rank'] = roster['risk_adjusted_score'].rank(ascending=False)
    roster = roster.sort_values(by='final_rank')

    # Add tiering
    roster = assign_tiers(roster)

    return roster



def assign_tiers(df: pd.DataFrame, score_column: str = 'risk_adjusted_score', threshold: float = 2.0) -> pd.DataFrame:
    df = df.sort_values(by=score_column, ascending=False).copy()
    scores = df[score_column].values
    tiers = [1]
    for i in range(1, len(scores)):
        if scores[i - 1] - scores[i] > threshold:
            tiers.append(tiers[-1] + 1)
        else:
            tiers.append(tiers[-1])
    df['tier'] = tiers
    return df

# SIMULATION







# -------------------- Execution --------------------

if __name__ == "__main__":
    roster = build_roster("your_dataset.csv")
    roster.to_csv("rookie_sophomore_full_roster.csv", index=False)
    print(roster[['player', 'position', 'role', 'mean_projection', 'risk_adjusted_score', 'final_rank']])
