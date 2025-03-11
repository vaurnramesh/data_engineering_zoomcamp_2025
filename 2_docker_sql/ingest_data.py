import os
import argparse
import pandas as pd
from sqlalchemy import create_engine

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'

    # download the csv
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    ## Using a iterator to break the data into chunks such that the database does not break
    df_iter = pd.read_csv(csv_name, low_memory=False, iterator=True, chunksize=100000, compression='gzip')
    df = next(df_iter)

    # Converting the dates into date time as pandas isn't able to recognise it
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


    
    engine.connect()

    # Getting an overview of the table to create a schema in DDL
    print(pd.io.sql.get_schema(df, name=table_name, con=engine))

    # Inserting just the column names
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # Inserting first chunk
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # Insert all remaining chunks
    for chunk in df_iter:
        chunk.tpep_pickup_datetime = pd.to_datetime(chunk.tpep_pickup_datetime)
        chunk.tpep_dropoff_datetime = pd.to_datetime(chunk.tpep_dropoff_datetime)

        chunk.to_sql(name=table_name, con=engine, if_exists='append')
        print('Inserted another chunk...')
    print("Data ingestion complete")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host name for postgres')
    parser.add_argument('--port', help='port name for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='table name for postgres')
    parser.add_argument('--url', help='user of the csv file')

    args = parser.parse_args()
    main(args)
