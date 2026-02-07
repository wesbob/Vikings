import os
import pandas as pd
from sqlalchemy import create_engine

csv_file_path = 'vikings_pbp_full.csv'
password = os.environ.get('POSTGRES_PASSWORD')
database_connection = f'postgresql://postgres:{password}@localhost:5432/vikings_analytics'


def load_csv_to_db(csv_path, db_connection, table_name='plays'):
    # Create a database engine
    engine = create_engine(db_connection)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)
    
    # Load the DataFrame into the database
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data loaded into table '{table_name}' successfully.")
if __name__ == "__main__":
    load_csv_to_db(csv_file_path, database_connection)




