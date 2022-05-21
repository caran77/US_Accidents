import pandas as pd


def get_accidents_dataset():
    df = pd.read_csv('files/US_Accidents_Dec21_updated.csv')
    return df
