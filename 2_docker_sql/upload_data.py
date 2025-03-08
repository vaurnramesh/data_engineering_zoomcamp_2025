import pandas as pd
from sqlalchemy import create_engine

## Using a iterator to break the data into chunks such that the database does not break
df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', low_memory=False, iterator=True, chunksize=100000)
df = next(df_iter)

# Converting the dates into date time as pandas isn't able to recognise it
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

# Getting an overview of the table to create a schema in DDL
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

# Inserting just the column names
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

# Inserting first chunk
df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

# Insert all remaining chunks
for chunk in df_iter:
    chunk.tpep_pickup_datetime = pd.to_datetime(chunk.tpep_pickup_datetime)
    chunk.tpep_dropoff_datetime = pd.to_datetime(chunk.tpep_dropoff_datetime)

    chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
    print('Inserted another chunk...')
print("Data ingestion complete")