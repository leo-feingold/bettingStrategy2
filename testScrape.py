import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from datetime import datetime



# Set up the Selenium WebDriver
driver = webdriver.Safari()

# Navigate to the URL
url = 'https://www.actionnetwork.com/odds'
driver.get(url)

# Give the page some time to load
time.sleep(10)

# Use WebDriverWait to wait for the elements to be present
wait = WebDriverWait(driver, 20)

try:
    odds = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.css-1qynun2.e1qivpas2')))
    teams = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.game-info__team--mobile span')))
    books = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img[alt*="logo"]')))

except Exception as e:
    print(f"Error occurred: {e}")
    driver.quit()
    exit()

odds_values = [odd.text for odd in odds]
team_names = [team.text for team in teams]
book_names_from_page = [book.get_attribute('alt') for book in books]
# Returns: 'FanDuel NY', 'BetMGM NY', 'DK NJ', 'Caesars NY', 'BetRivers NY', 'Fanatics NY', 'BetMGM NJ

if book_names_from_page == ['FanDuel NY logo', 'BetMGM NY logo', 'DK NJ logo', 'Caesars NY logo', 'BetRivers NY logo', 'Fanatics NY logo', 'BetMGM NJ logo']:
    #normal order: best odds, fanduel, betmgm, DK, caesars, betrivers, bally bet ny (no logo), fanatics (Empty), resorts world bet ny (empty), betmgm
    print("Pre-set columns look okay. Continuing scrape.")
else:
    print("Error with pre-set columns. See web page.")
    raise ValueError(f"Scraped columns looked like: {book_names_from_page}")

# will need to update this every time
#book_names = ["Best Odds", "Fanduel (NY)", "BetMGM (NY)", "Draft Kings (NJ)", "Caesars (NY)", "BetRivers (NY)", "Bally Bet NY", "BetMGM (NJ)"]
book_names = ["Best Odds", "Fanduel (NY)", "BetMGM (NY)", "Draft Kings (NJ)", "BetRivers (NY)", "Bally Bet NY", "BetMGM (NJ)"]


# Debugging outputs
print(f"Odds found ({len(odds_values)}): {odds_values}")
print(f"Teams found ({len(team_names)}): {team_names}")
print(f"Books found ({len(book_names)}): {book_names}")

driver.quit()

# Check if the number of odds matches the expected count
expected_odds_count = len(team_names) * len(book_names)
if len(odds_values) != expected_odds_count:
    print("Warning: The number of odds values does not match the expected count based on teams and books.")
    exit()

# Create a dictionary to hold the data
odds_dict = {team: {book: None for book in book_names} for team in team_names}

# Populate the dictionary with odds
odds_index = 0
for i in range(0, len(team_names), 2):  # Step through teams in pairs
    for book in book_names:
        if odds_index < len(odds_values):
            odds_dict[team_names[i]][book] = odds_values[odds_index]
            odds_dict[team_names[i+1]][book] = odds_values[odds_index+1]
            odds_index += 2

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(odds_dict, orient='index')

# Save the DataFrame to a CSV file
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

df.to_csv(f'{now}_odds_data.csv')

print('Data has been saved to odds_data.csv')