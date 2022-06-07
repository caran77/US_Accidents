import numpy as np
import pandas as pd

from data.data import get_file

PATH = 'files/'


def get_data_from_period_by_state(period):
    df_by_period = get_file(period + '.csv')
    df_by_period_by_severity = df_by_period.groupby('StateName')['Severity'].mean()
    result = pd.DataFrame(df_by_period_by_severity)
    percentile_33 = np.percentile(result[result['Severity']
                                  .notnull()]['Severity'], 33, axis=0)
    percentile_66 = np.percentile(result[result['Severity']
                                  .notnull()]['Severity'], 66, axis=0)

    result.loc[result['Severity'] >= percentile_66, 'Severity_cat'] = '2'
    result.loc[result['Severity'] < percentile_66, 'Severity_cat'] = '1'
    result.loc[result['Severity'] < percentile_33, 'Severity_cat'] = '0'
    result[['Severity_cat']].to_csv(PATH + 'severity_' + period + '.csv')


def get_black_points(period):
    df_by_period = get_file(period + '.csv')
    df_by_period['Start_Lat_Calc'] = round(df_by_period['Start_Lat'], 0)
    df_by_period['Start_Lng_Calc'] = round(df_by_period['Start_Lng'], 0)
    black_points = pd.DataFrame({'count': df_by_period.groupby(["Start_Lat_Calc", "Start_Lng_Calc", "City"]).size()}) \
        .reset_index()
    #    df_by_period.groupby(['Start_Lat_Calc', 'Start_Lng_Calc']).size()
    black_points = black_points.sort_values(by='count', ascending=False).head(100)
    black_points.rename(columns={'Start_Lat_Calc': 'lat', 'Start_Lng_Calc': 'lon', 'count': 'count', 'City': 'place'},
                        inplace=True)
    black_points.to_csv(PATH + 'black_points_' + period + '.csv', index=False, sep=',')
    print(df_by_period)


# get_data_from_period_by_state('2021')
get_black_points('2021')
