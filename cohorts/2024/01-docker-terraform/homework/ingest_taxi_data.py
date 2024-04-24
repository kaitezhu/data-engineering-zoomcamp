#!/usr/bin/env python
# coding: utf-8

import os, argparse, sys

from time import time

import pandas as pd
from sqlalchemy import create_engine
import pyarrow.parquet as pq

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    tb = params.tb
    url = params.url
    
    # url = "cohorts/2024/01-docker-terraform/homework/taxi+_zone_lookup.csv"
    # Get the name of the file from url, https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
    file_name = url.rsplit('/', 1)[-1].strip()
    print(f'Downloading {file_name} ...')

    # create SQL engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read file based on csv or parquet
    if '.csv' in file_name:
        df = pd.read_csv(file_name, nrows=10)
        df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)
    elif '.parquet' in file_name:
        file = pq.ParquetFile(file_name)
        df = next(file.iter_batches(batch_size=10)).to_pandas()
        df_iter = file.iter_batches(batch_size=100000)
    else:
        print('Error. Only .csv or .parquet files allowed.')
        sys.exit()

    # create the table schema
    df.head(0).to_sql(name=tb, con=engine, if_exists='replace')

    # insert values
    t_start = time()
    count = 0

    for batch in df_iter:
        count += 1

        if '.parquet' in file_name:
            batch_df = batch.to_pandas()
        else:
            batch_df = batch

        print(f'inserting batch {count}...')

        b_start = time()
        batch_df.to_sql(name=tb, con=engine, if_exists='append')
        b_end = time()

        print(f'inserted! time taken {b_end-b_start:10.3f} seconds. \n')
    
    t_end = time()
    print(f'completed! total time taken {t_end-t_start:10.3f} seconds for {count} batches. \n')


if __name__ == '__main__':
    # parsing arguments
    parser = argparse.ArgumentParser(description='Loading data from .parquet file link to a Postgres database.')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password name for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--tb', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='URL for .parquet file')

    args = parser.parse_args()

    main(args)