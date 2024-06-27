import pandas as pd

def load_data(csv):
    df = pd.read_csv(csv)
    return df

def process_data(df):
    df = df.apply(lambda x: x.replace('+', '') if isinstance(x, str) else x)
    df[["Best Odds","Fanduel (NY)","BetMGM (NY)","Draft Kings (NJ)","Caesars (NY)","BetRivers (NY)","Bally Bet NY","BetMGM (NJ)"]] = df[["Best Odds","Fanduel (NY)","BetMGM (NY)","Draft Kings (NJ)","Caesars (NY)","BetRivers (NY)","Bally Bet NY","BetMGM (NJ)"]].apply(pd.to_numeric)
    return df

def calc_implied_prob(odds):
    if odds > 0:
        return ((100/(odds + 100)) * 100)
    else:
        odds = abs(odds)
        return ((odds/(odds + 100)) * 100)

def append_IP_to_df(df):
    df["implied_probability"] = df["Best Odds"].apply(calc_implied_prob)
    return df

def sum_implied_probabilities(df):
    teams = df.index.tolist()
    summed_probabilities = []
    for i in range(0, len(teams), 2):
        team1, team2 = teams[i], teams[i + 1]
        team1_prob = df.loc[team1, "implied_probability"]
        team2_prob = df.loc[team2, "implied_probability"]
        summed_probabilities.append((team1, team2, team1_prob + team2_prob))
    return summed_probabilities

def main():
    csv = "/Users/leofeingold/Desktop/bettingStrategy2/Data_CSVs/odds_data.csv"
    data = load_data(csv)
    data = process_data(data)

    data.index = data.iloc[:, 0]
    data = data.drop(data.columns[0], axis=1)

    data = append_IP_to_df(data)
    probabilities = sum_implied_probabilities(data)
    print(probabilities)
    for match in probabilities:
        team1, team2, total_prob = match
        if total_prob < 100:
            print(f"\n{team1} vs {team2}: Total Implied Probability = {total_prob:.2f}%")
    print(f"\n{data.head()}")
    

if __name__ == "__main__":
    main()