# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd
from bs4 import BeautifulSoup

def clean_distance_data(soup):
    '''Step 1:
       Using Pandas to get a dataframe of all the values.'''

    dist_df = pd.DataFrame()
    start_date_col = []
    end_date_col = []
    tot_dist_col = []
    source_col = []

    distance = soup.findAll(
            'Record', {'type': 'HKQuantityTypeIdentifierDistanceWalkingRunning'
                       })

    for num in distance:
        start_date_col.append(num['startDate'])
        end_date_col.append(num['endDate'])
        tot_dist_col.append(num['value'])
        source_col.append(num['sourceName'])

    dist_df.loc[:, 'start_date'] = start_date_col
    dist_df.loc[:, 'end_date'] = end_date_col
    dist_df.loc[:, 'tot_dist'] = tot_dist_col
    dist_df.loc[:, 'source'] = source_col

    dist_df.loc[:, 'tot_dist'] = dist_df.tot_dist.astype(float)

    dist_df.sort_values(by=['start_date', 'end_date'], inplace=True)
    dist_df = dist_df[dist_df['tot_dist'] > 1e-4]
    dist_df.reset_index(inplace=True)
    dist_df.drop(columns=['index'], inplace=True)

    return dist_df


def split_distance_between_days(df):
    '''Step : 4
       Split distance between days, in case a measurement starts on one day
       and finishes the following or more days from that time.'''

    i = 0
    while i < len(df) - 1:

        if (df.end_date[i] - pd.Timedelta(1, unit='D') == df.start_date[i]):

            st_dt, st_tm, end_dt, end_tm, tot_di, dur, sauce = df.iloc[i]

            dist_per_hour = tot_di / (end_tm + (24.0 - st_tm))

            tot_di_1 = dist_per_hour * (24.0 - st_tm)
            tot_di_2 = dist_per_hour * end_tm

            df.loc[i + .1] = [end_dt, 0.0, end_dt, end_tm,
                              tot_di_2, end_tm, sauce]

            df.loc[i] = [st_dt, st_tm, st_dt, 24.0,
                         tot_di_1, (24.0 - st_tm), sauce]

            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)

            i += 1

        elif (df.end_date[i] - pd.Timedelta(2, unit='D') == df.start_date[i]):

            st_dt, st_tm, end_dt, end_tm, tot_di, dur, sauce = df.iloc[i]

            dist_per_hour = tot_di / (end_tm + 24.0 + (24.0 - st_tm))

            tot_di_1 = dist_per_hour * (24.0 - st_tm)
            tot_di_2 = dist_per_hour * 24.0
            tot_di_3 = dist_per_hour * end_tm

            dt_2 = end_dt - pd.Timedelta(1, unit='D')

            df.loc[i + .1] = [dt_2, 0.0, dt_2, 24.0,
                              tot_di_2, 24.0, sauce]

            df.loc[i + .2] = [end_dt, 0.0, end_dt, end_tm,
                              tot_di_3, end_tm, sauce]

            df.loc[i] = [st_dt, st_tm, st_dt, 24.0,
                         tot_di_1, (24.0 - st_tm), sauce]

            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)
            i += 1

        else:
            i += 1

    return df


def trim_distance_from_overlapping_times(df):
    '''Step : 6
       Correct total distance and times from overlapping times.

       To trim distance, make sure to check if start date for the same row are
       the same and make sure the following row has the same starting and
       ending date.

       Also, the starting time of the following row has to be less than ending
       time for the row to check and the ending time for the following row has
       to be greater.

       Once the distance is trimmed, if the remaining distance is less than
       1e-4, drop the row.

       All distances are in miles. 1e-4 miles is equal to roughly 6 inches.'''

    i = 0

    while i < len(df) - 1:

        if (df.start_date[i] == df.end_date[i]) and (
                df.start_date[i] == df.end_date[i + 1]) and(
                df.start_date[i] == df.start_date[i + 1]) and (
                df.start_time[i + 1] < df.end_time[i]) and (
                df.end_time[i + 1] >= df.end_time[i]):

            dist_per_hour = df.tot_dist[i + 1] / \
                (df.end_time[i + 1] - df.start_time[i + 1])
            dist_adjust = (df.end_time[i] -
                           df.start_time[i + 1]) * dist_per_hour

            df.loc[(i + 1), 'tot_dist'] = df.tot_dist[i + 1] - dist_adjust
            df.loc[(i + 1), 'start_time'] = df.end_time[i]
            df.loc[(i + 1), 'duration'] = df.end_time[i + 1] - \
                df.start_time[i + 1]
            df.loc[i, 'duration'] = df.end_time[i] - df.start_time[i]

            if df.tot_dist[i + 1] < 1e-4:
                df.drop(index=(i + 1), inplace=True)
                df.reset_index(inplace=True)
                df.drop(columns=['index'], inplace=True)
            else:
                i += 1

        else:
            i += 1

    return df
