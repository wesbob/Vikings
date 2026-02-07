import nfl_data_py as nfl
import pandas as pd

# Pull play-by-play data for Randy Moss era (1999-2004, 2010) and recent seasons (2023-2025)
# This takes a minute - it's downloading a lot of data
# Note: NFLverse data starts from 1999, so Moss's 1998 rookie season isn't available
seasons = [1999, 2000, 2001, 2002, 2003, 2004, 2010, 2023, 2024, 2025]
print(f"Pulling play-by-play data for {len(seasons)} seasons: {seasons}...")
pbp = nfl.import_pbp_data(seasons)

print(f"Total plays: {len(pbp):,}")
print(f"Columns: {len(pbp.columns)}")

# Filter to Vikings games (home or away)
vikings = pbp[(pbp['home_team'] == 'MIN') | (pbp['away_team'] == 'MIN')]
print(f"Vikings plays: {len(vikings):,}")

keyColumns = [
    'game_id', 'play_id', 'play_type', 'desc', 'yards_gained', 'posteam', 'down', 'ydstogo', 'yardline_100',
    'fourth_down_converted', 'fourth_down_failed', 'posteam', 'score_differential', 'epa'
]
# Filter to just 4th down plays
fourthDowns = vikings[vikings['down'] == 4]
print(f"Vikings 4th down plays: {len(fourthDowns):,}")

# Print sample row
print("\n--- Sample row ---")
print(fourthDowns[keyColumns].head(1).to_string())

# Save to csv
output_path = 'vikings_pbp_full.csv'
vikings.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")