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

def calc_bets(df, game, capital_per_bet):
    team1, team2, total_prob = game
    team1_prob = df.loc[team1, "implied_probability"]
    team2_prob = df.loc[team2, "implied_probability"]
    if ((team1_prob + team2_prob) != total_prob):
        print("Something is wrong...")
    else:
        team1_ratio = team1_prob/total_prob
        team2_ratio = team2_prob/total_prob
        team1_investment = team1_ratio * capital_per_bet
        team2_investment = team2_ratio * capital_per_bet

    return team1_investment, team2_investment

def calc_payout(capital_per_bet, odds):
    if odds < 0:
        odds = abs(odds)
        profit = (100/odds * capital_per_bet)
    else:
        profit = (odds/100 * capital_per_bet)
    return profit

def main():
    capital_per_bet = 1000
    csv = "/Users/leofeingold/Desktop/bettingStrategy2/Data_CSVs/odds_data.csv"
    data = load_data(csv)
    data = process_data(data)

    data.index = data.iloc[:, 0]
    data = data.drop(data.columns[0], axis=1)

    data = append_IP_to_df(data)
    probabilities = sum_implied_probabilities(data)
    print(probabilities)
    for game in probabilities:
        team1, team2, total_prob = game
        if total_prob < 100:
            print(f"\n{team1} vs {team2}: Total Implied Probability = {total_prob:.2f}%")
            team1_investment, team2_investment = calc_bets(data, game, capital_per_bet)
            team1_odds = data.loc[team1, "Best Odds"]
            team2_odds = data.loc[team2, "Best Odds"]
            print(f"{team1} Bet Size: {team1_investment}, {team2} Bet Size: {team2_investment}")
            print(f"{team1} Odds: {team1_odds}, {team2} Odds: {team2_odds}")
            profit = calc_payout(team1_investment, team1_odds) - team2_investment
            # (both work)
            #profit = calc_payout(team2_investment, team2_odds) - team1_investment
            print(f"Guaranteed Profit: {profit}")
            
            if ((team1_investment+team2_investment) != capital_per_bet):
                print("Something is wrong...")
            else:
                print(f"Guaranteed ROI (%): {(profit/(capital_per_bet)) * 100}%")

if __name__ == "__main__":
    main()