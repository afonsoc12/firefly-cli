from datetime import datetime
from io import StringIO
from pathlib import Path

import pandas as pd


def parse_transaction_to_df(input):
    if isinstance(input, str):
        cols = ['amount', 'description', 'source_name', 'destination_name', 'category', 'budget']
        data = pd.read_csv(StringIO(input), header=None)

        # Add remaining columns None
        data.columns = cols[:data.shape[1]]
        data = pd.concat([data, pd.DataFrame([[None for _ in cols[data.shape[1]:]]], columns=cols[data.shape[1]:])],
                         axis=1)
        data.index = [datetime.now()]

        # Convert all to string and strip edges
        data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return data


def parse_csv_to_df(file):
    """Parses a .csv file to dataframe.

    Assumes that the file exists
    """
    cols = ['date', 'amount', 'description', 'source_name', 'destination_name', 'category', 'budget', 'attachment', 'processed']

    data = pd.read_csv(file, header=True)

    if data.columns.tolist()[:4] not in cols:
        print('[ERROR] Columns of the file don\'t match!')
        print('\t> Found: {}'.format(' | ' .join(cols)))
        print('\t> Expected: {}'.format(' | ' .join(cols)))
        return None

    # Add remaining columns None
    data.columns = cols[:data.shape[1]]
    data = pd.concat([data, pd.DataFrame([[None for _ in cols[data.shape[1]:]]], columns=cols[data.shape[1]:])],
                         axis=1)
    data.index = [datetime.now()]

    # Convert all to string and strip edges
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    return data
