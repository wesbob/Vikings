import os
import pandas as pd
from sqlalchemy import create_engine

csv_file_path = 'moss_1998_games.csv'
password = os.environ.get('POSTGRES_PASSWORD')
database_connection = f'postgresql://postgres:{password}@localhost:5432/vikings_analytics'


def load_1998_stats(csv_path, db_connection):
    # Create a database engine
    engine = create_engine(db_connection)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Load the DataFrame into a separate table for 1998 game stats
    df.to_sql('moss_1998_games', engine, if_exists='replace', index=False)
    print(f"1998 Randy Moss game stats loaded into table 'moss_1998_games' successfully.")
    print(f"Total games: {len(df)}")
    print(f"Season totals: {df['receptions'].sum()} rec, {df['receiving_yards'].sum()} yds, {df['receiving_tds'].sum()} TDs")


if __name__ == "__main__":
    load_1998_stats(csv_file_path, database_connection)
