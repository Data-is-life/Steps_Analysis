# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


def cleaning_data(file_name):
    '''
    Step 1:
    Using BeautifulSoup to get parse the information from .xml file.
    Using Pandas to get a dataframe of all the values.
    '''

    dist_df = pd.DataFrame()
    start_date_col = []
    end_date_col = []
    tot_dist_col = []
    source_col = []

    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'lxml-xml')

    distance = soup.findAll(
        'Record', {'type': 'HKQuantityTypeIdentifierDistanceWalkingRunning'})

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


def clean_start_end_times(dist_df, s_o_e):
    '''
    Step : 2
    Separate out end and start times to different dataframes and remove
    unnecessary items.
    '''

    d_df = dist_df[(s_o_e + '_date')].str.split(' ', expand=True)
    d_df.columns = [(s_o_e + '_date'), (s_o_e + '_time'), 'time_zone']

    d_df.drop(columns=['time_zone'], inplace=True)
    d_df.loc[:, s_o_e+'_date'] = pd.to_datetime(
        d_df[s_o_e + '_date'], format='%Y/%m/%d')

    d_df.loc[:, s_o_e+'_time'] = pd.to_timedelta(d_df[s_o_e + '_time'])

    return d_df


def clean_duration(dist_df):
    '''
    Step : 3
    Create a new dataframe combining the start and end times.
    '''

    sd_df = clean_start_end_times(dist_df, 'start')
    ed_df = clean_start_end_times(dist_df, 'end')
    dur_df = pd.concat([sd_df, ed_df], axis=1)

    dur_df.loc[:, 'sdt'] = dur_df['start_date'] + dur_df['start_time']
    dur_df.loc[:, 'edt'] = dur_df['end_date'] + dur_df['end_time']
    dur_df.loc[:, 'duration'] = dur_df['edt'] - dur_df['sdt']
    dur_df.drop(columns=['sdt', 'edt'], inplace=True)

    return dur_df


def remove_overlap_time_rows(df):
    '''
    Step : 5
    Remove all the rows that overlap times.
    '''

    i = 0
    while i < len(df) - 1:
        if (df.start_date[i] == df.end_date[i]) and (
                df.start_date[i] == df.end_date[i + 1]) and (
                df.start_date[i] == df.start_date[i + 1]) and (
                df.start_time[i] <= df.start_time[i + 1]) and (
                df.end_time[i] >= df.end_time[i + 1]):

            df.drop(index=(i + 1), inplace=True)
            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)

        else:
            i += 1

    return df


def trim_distance_from_overlapping_times(df):
    '''
    Step : 6
    Correct total distance and times from overlapping times.
    '''

    i = 0
    while i < len(df) - 1:
        if (df.start_date[i] == df.end_date[i]) and (
                df.start_date[i] == df.end_date[i + 1]) and(
                df.start_date[i] == df.start_date[i + 1]) and (
                df.start_time[i + 1] <= df.end_time[i]) and (
                df.end_time[i + 1] >= df.end_time[i]):

            dist_per_hour = df.tot_dist[
                i + 1] / (df.end_time[i + 1] - df.start_time[i + 1])

            dist_adjust = (df.end_time[i] -
                            df.start_time[i + 1]) * dist_per_hour

            dist_adjust = dist_adjust

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


def split_distance_between_days(df):
    '''
    Step : 4
    Split distance between days, in case a measurement starts on one day
    and finishes the following or more days from that time.
    '''

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


def print_remainder(df):
    '''
    This is just to check how many rows are left in the dataframe,
    sum of total distance, and how many instances are left that start
    on one day and finishes another day.
    '''

    print(f'Total Rows = {len(df)}')
    print(f'Total Steps = {df.tot_dist.sum()}')
    print(f"start_date != end_date: {len(df[df['start_date']!=df['end_date']])}")


def print_all_info(df):
    '''
    Get the information of any dataframe.
    '''

    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^df.head()^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(df.head())
    print('\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^df.tail()^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(df.tail())
    print('\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^df.describe()^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(df.describe())
    print('\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^df.info()^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(df.info())


def reset_df_uno(df):
    '''
    Found this convinient, since removing and adding rows every function could
    lead to missing indexes and data not being in correct order.
    '''

    df.sort_values(by=['start_date', 'start_time'], inplace=True)
    df = df[df['tot_dist'] > 1e-4]
    df.loc[:, 'duration'] = np.where(df['start_date'] == df['end_date'],
      (df['end_time'] - df['start_time']), df['duration'])
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    return df


def reset_df_dos(df):
    '''
    Found this convinient, since removing and adding rows every function could
    lead to missing indexes and data not being in correct order.
    '''

    df.sort_values(by=['start_date', 'end_time'], inplace=True)
    df = df[df['tot_dist'] > 1e-4]
    df.loc[:, 'duration'] = np.where(df['start_date'] == df['end_date'],
      (df['end_time'] - df['start_time']), df['duration'])
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    return df

