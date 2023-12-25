import pandas as pd
from math import ceil


def request_procession(lowest: int, highest: int) -> int:
    '''Counts and returns the mean price of Mercedes cars of
    the year from the given period'''

    # Clean dataset with all columns except 'year' and 'price' removed.
    # That is to save memory.
    df = pd.read_csv("year_price_slice.csv")

    # Cut down irrelevant years
    df = df[(df['year'] >= lowest) & (df['year'] <= highest)]

    return ceil(df['price'].mean())
