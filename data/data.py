import numpy as np
import pandas as pd

PATH = 'files/'


def get_accidents_dataset():
    df = pd.read_csv(PATH + 'US_Accidents_Dec21_updated.csv')
    return df


def get_states():
    df = pd.read_csv(PATH + 'us_states.csv')
    return df


def get_states_lived():
    df = pd.read_csv(PATH + 'stateslived.csv')
    return df


def get_file(file_name):
    df = pd.read_csv(PATH + file_name, sep=',')
    return df


def export_dataset(df):
    export_years(df)
    export_months(df)


def export_months(df):
    distinct_dates = df['Start_Time'].str[:7].unique()
    for dd in distinct_dates:
        data_for_month = df[df['Start_Time'].str[:7] == dd]
        data_for_month.to_csv(PATH + dd + '.csv', index=False, sep=',')


def export_years(df):
    distinct_dates = df['Start_Time'].str[:4].unique()
    for dd in distinct_dates:
        data_for_month = df[df['Start_Time'].str[:4] == dd]
        data_for_month.to_csv(PATH + dd + '.csv', index=False, sep=',')


def export_dataset_grouped_by_year(df):
    distinct_dates = df['Start_Time'].str[:4].unique()
    distinct_states = df['StateName'].unique()
    df_output = pd.DataFrame()
    for ds in np.sort(distinct_states):
        dict_to_output = {'Name': ds}
        for dd in np.sort(distinct_dates):
            number_of_values = round(df[(df['Start_Time'].str[:4] == dd) & (df['StateName'] == ds)]
                                     ['Severity'].mean(), 2)
            dict_to_output[dd] = number_of_values
        df_output = df_output.append(dict_to_output, ignore_index=True)
    df_output.to_csv(PATH + 'severity_by_state_and_year.csv', index=False, sep=',')


def export_black_points_by_year(df):
    df['Latitude'] = round(df['Start_Lat'], 1)
    df['Longitude'] = round(df['Start_Lng'], 1)
    df['year'] = df['Start_Time'].str[:4]
    df_to_calculate = df[['Latitude', 'Longitude', 'year', 'City']]
    df_to_calculate = df_to_calculate.groupby(['Latitude', 'Longitude', 'year', 'City'])\
        .size().reset_index(name='count')
    distinct_dates = df['Start_Time'].str[:4].unique()
    distinct_dates = np.sort(distinct_dates)
    df_pivot = df_to_calculate.pivot(index=['Latitude', 'Longitude', 'City'], columns='year', values='count').reset_index()
    df_pivot = df_pivot.fillna(0)
    df_to_print = pd.DataFrame()
    for dd in distinct_dates:
        df_by_year = df_pivot.sort_values(by=dd, ascending=False).head(50)
        df_to_print = df_to_print.append(df_by_year)
    df_to_print.to_csv(PATH + 'black_points_by_year.csv', index=False, sep=',')
