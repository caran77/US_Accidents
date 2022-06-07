import numpy as np
import pandas as pd


def prepare_dataset(df: pd.DataFrame, df_states: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(df, df_states, how="left", on=["State"])
    df = prepare_affected_area(df)
    df = affected_area_category(df)
    df = distance_category(df)
    df = temperature_category(df)
    df = wind_chill_category(df)
    df = humidity_category(df)
    df = pressure_category(df)
    df = visibility_category(df)
    df = wind_speed_category(df)
    df = precipitation_category(df)
    return df


def affected_area_category(df: pd.DataFrame) -> pd.DataFrame:
    return category_column(df, 'Affected_area', 'Affected_area_cat')


def distance_category(df: pd.DataFrame) -> pd.DataFrame:
    return category_column(df, 'Distance(mi)', 'Distance_cat')


def temperature_category(df: pd.DataFrame) -> pd.DataFrame:
    return category_column(df, 'Temperature(F)', 'Temperature_cat')


def wind_chill_category(df: pd.DataFrame) -> pd.DataFrame:
    return category_column(df, 'Wind_Chill(F)', 'Wind_Chill_cat')


def humidity_category(df: pd.DataFrame) -> pd.DataFrame:
    return category_column(df, 'Humidity(%)', 'Humidity_cat')


def pressure_category(df: pd.DataFrame) -> pd.DataFrame:
    return category_column(df, 'Pressure(in)', 'Pressure_cat')


def visibility_category(df: pd.DataFrame) -> pd.DataFrame:
    return category_column(df, 'Visibility(mi)', 'Visibility_cat')


def wind_speed_category(df: pd.DataFrame) -> pd.DataFrame:
    return category_column(df, 'Wind_Speed(mph)', 'Wind_Speed_cat')


def precipitation_category(df: pd.DataFrame) -> pd.DataFrame:
    return category_column(df, 'Precipitation(in)', 'Precipitation_cat')


def category_column(df: pd.DataFrame, column: str, column_categorized: str) -> pd.DataFrame:
    percentile_33 = np.percentile(df[df[column].notnull()][column], 33, axis=0)
    percentile_66 = np.percentile(df[df[column].notnull()][column], 66, axis=0)
    df.loc[df[column].isnull(), column_categorized] = 'NaN'
    df.loc[df[column] > percentile_66, column_categorized] = 'HIGH'
    df.loc[df[column] <= percentile_66, column_categorized] = 'MEDIUM'
    df.loc[df[column] <= percentile_33, column_categorized] = 'LOW'
    return df


def prepare_affected_area(df: pd.DataFrame) -> pd.DataFrame:
    latitude_difference = round_abs(df['Start_Lat'] - df['End_Lat'])
    longitude_difference = round_abs(df['Start_Lng'] - df['End_Lng'])
    df['Affected_area'] = latitude_difference * longitude_difference
    return df


def round_abs(value):
    return round(abs(value), 7)
