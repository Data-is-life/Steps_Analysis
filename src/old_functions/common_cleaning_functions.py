# Author: Mohit Gangwani
# Date: 11/13/2018
# Git-Hub: Data-is-Life

import pandas as pd
import numpy as np
from time import time


def clean_start_end_times(df, s_o_e):
    '''Separate out end and start times to different dataframes and remove
       timezone. Also split the date and time to two different columns.'''

    tt = time()
    d_df = df[(s_o_e + '_date')].str.split(' ', expand=True)
    d_df.columns = [(s_o_e + '_date'), (s_o_e + '_time'), 'time_zone']

    d_df.drop(columns=['time_zone'], inplace=True)
    d_df.loc[:, s_o_e + '_date'] = pd.to_datetime(
        d_df[s_o_e + '_date'], format='%Y/%m/%d')

    d_df.loc[:, s_o_e + '_time'] = pd.to_timedelta(d_df[s_o_e + '_time'])
    print(f'clean_start_end_times {time()-tt}')

    return d_df


def clean_duration(df):
    '''Step : 2
       Create a new dataframe combining the start and end times.'''

    tt = time()
    sd_df = clean_start_end_times(df, 'start')
    ed_df = clean_start_end_times(df, 'end')
    dur_df = pd.concat([sd_df, ed_df], axis=1)

    dur_df.loc[:, 'sdt'] = dur_df['start_date'] + dur_df['start_time']
    dur_df.loc[:, 'edt'] = dur_df['end_date'] + dur_df['end_time']
    dur_df.loc[:, 'duration'] = dur_df['edt'] - dur_df['sdt']
    dur_df.drop(columns=['sdt', 'edt'], inplace=True)
    print(f'clean_duration {time()-tt}')

    return dur_df


def clean_columns_conv_to_numeric(steps_df, dist_df, floors_df, dur_stp_df,
                                  dur_dst_df, dur_flt_df):
    '''Step : 3
       First combine duration dataframe and the dataframe with all the values.
       Second keep only the columns needed.
       Third reset the and sort the dataframes by date and time.
       Fourth convert the time and duration to numeric values. numeric values.
       are a lot easier to work with than time deltas.'''

    tt = time()
    steps_df.drop(columns=['start_date', 'end_date'], inplace=True)
    dist_df.drop(columns=['start_date', 'end_date'], inplace=True)
    floors_df.drop(columns=['start_date', 'end_date'], inplace=True)

    stp_df = pd.concat([steps_df, dur_stp_df], axis=1)
    dst_df = pd.concat([dist_df, dur_dst_df], axis=1)
    flr_df = pd.concat([floors_df, dur_flt_df], axis=1)

    stp_df = stp_df[['start_date', 'start_time', 'end_date', 'end_time',
                     'num_steps', 'duration', 'source']].copy()
    dst_df = dst_df[['start_date', 'start_time', 'end_date', 'end_time',
                     'tot_dist', 'duration', 'source']].copy()
    flr_df = flr_df[['start_date', 'start_time', 'end_date', 'end_time',
                     'num_floors', 'duration', 'source']].copy()

    stp_df = reset_steps_uno(stp_df)
    dst_df = reset_distance_uno(dst_df)
    flr_df = reset_floors_uno(flr_df)

    cols_to_change = ['start_time', 'end_time', 'duration']
    for col in cols_to_change:
        stp_df.loc[:, col] = pd.to_numeric(stp_df[col]) / 3.6e12
        dst_df.loc[:, col] = pd.to_numeric(dst_df[col]) / 3.6e12
        flr_df.loc[:, col] = pd.to_numeric(flr_df[col]) / 3.6e12
    print(f'clean_columns_conv_to_numeric {time()-tt}')
    return stp_df, dst_df, flr_df


def remove_overlap_time_rows(df):
    '''Step : 5
       Remove all the rows that overlap times.

       To remove overlapping rows, make sure to check if start date for the
       same row are the same and make sure the following row has the same
       starting and ending date.

       Also, the starting time of the following row has to be greater than or
       equal to the starting time for the row and the ending time for the
       following row has to be less than or equal to the row to check.

       Once the row is identified, drop the row, and reset index.

       Using while loop, since the function can keep checking the same row
       with the following rows.'''

    i = 0
    tt = time()
    while i < len(df) - 1:

        if (df.start_time[i] <= df.start_time[i+1]) and (
                df.end_time[i] >= df.end_time[i+1]) and (
                       df.start_date[i] == df.start_date[i+1]) and (
                                df.start_date[i] == df.end_date[i+1]) and (
                                         df.start_date[i] == df.end_date[i]):

            df.drop(index=(i+1), inplace=True)
            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)

        else:
            i += 1
    print(f'remove_overlap_time_rows {time()-tt}')
    return df


def trim_data_from_overlapping_times(sdf, ddf, fdf):
    '''Step : 6
       Correct total steps, distance, floors climbed, and times from
       overlapping times.

       To trim the data, making sure to check if start date for the same row
       are the same, also the following row has the same starting and
       ending date.

       In addition, the starting time of the following row has to be less than
       ending time for the row to check and the ending time for the following
       row has to be greater.

       Once the data is trimmed, the following logic is used to determine if
       the row need to be dropped:
       if the remaining steps or floors climbed are less than 0.4444,
       if the remaining distance is less than 8e-5.

       8e-5 miles = 0.4444 feet

       Rounding 0.4444 to an integer will be 0.'''

    i = 0
    tt = time()
    while i < len(df) - 1:
        if (df.start_time[i] <= df.start_time[i+1]) and (
                df.end_time[i] >= df.end_time[i+1]) and (
                       df.start_date[i] == df.start_date[i+1]) and (
                                df.start_date[i] == df.end_date[i+1]) and (
                                         df.start_date[i] == df.end_date[i]):

            stps_per_hr = sdf.num_steps[i+1] / (sdf.end_time[i+1] - sdf.start_time[i+1])
            dist_per_hr = ddf.num_steps[i+1] / (ddf.end_time[i+1] - ddf.start_time[i+1])
            flrs_per_hr = fdf.num_steps[i+1] / (fdf.end_time[i+1] - fdf.start_time[i+1])

            steps_adjust = (df.end_time[i] - df.start_time[i+1]) * stps_per_hr
            steps_adjust = (df.end_time[i] - df.start_time[i+1]) * stps_per_hr
            steps_adjust = (df.end_time[i] - df.start_time[i+1]) * stps_per_hr
            steps_adjust = round(steps_adjust)

            df.loc[i+1, 'num_steps'] = df.num_steps[i+1] - steps_adjust
            df.loc[i+1, 'start_time'] = df.end_time[i]
            df.loc[i+1, 'duration'] = df.end_time[i+1] - df.start_time[i+1]
            df.loc[i, 'duration'] = df.end_time[i] - df.start_time[i]

            if df['num_steps'][i+1] > 0.4444:
                df.drop(index=(i+1), inplace=True)
                df.reset_index(inplace=True)
                df.drop(columns=['index'], inplace=True)
            else:
                i += 1
        else:
            i += 1
    print(f'trim_steps_from_overlapping_times {time()-tt}')
    return df


def print_remaining(df, df_name):
    '''This is just to check how many rows are left in the dataframe,
       sum of total distance or steps, and how many instances are left that
       start on one day and finishes another day.'''

    print(f'Total Rows = {len(df)}')
    print(f'Total ' + df_name + ' = {df.tot_dist.sum()}')
    print(f"start_date != end_date: \
          {len(df[df['start_date'] != df['end_date']])}")


def print_all_info(df):
    '''Get the following information of any dataframe:
       1. First 5 rows
       2. Last 5 rows
       3. Information of the dataframe
       4. Types of data for each column'''

    print('^^^^^^^^^^^^^^^^^^^^^^^^df.head()^^^^^^^^^^^^^^^^^^^^^^^^')
    print(df.head())
    print('\n\n^^^^^^^^^^^^^^^^^^^^^^^^df.tail()^^^^^^^^^^^^^^^^^^^^^^^^')
    print(df.tail())
    print('\n\n^^^^^^^^^^^^^^^^^^^^^^df.describe()^^^^^^^^^^^^^^^^^^^^^^')
    print(df.describe())
    print('\n\n^^^^^^^^^^^^^^^^^^^^^^^^df.info()^^^^^^^^^^^^^^^^^^^^^^^^')
    print(df.info())


def reset_distance_uno(df):
    '''Found this convenient, since removing and adding rows every function
       could lead to missing indexes and data not being in correct order.'''

    df.sort_values(by=['start_date', 'start_time'], inplace=True)
    df = df[df['tot_dist'] > 1e-4].copy()
    df.loc[:, 'duration'] = np.where(df['start_date'] == df['end_date'],
                                     (df['end_time'] - df['start_time']),
                                     df['duration'])

    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)

    return df


def reset_distance_dos(df):
    '''Found this convenient, since removing and adding rows every function
       could lead to missing indexes and data not being in correct order.'''

    df.sort_values(by=['start_date', 'start_time'], inplace=True)
    df = df[df['duration'] > 5e-4].copy()
    df.loc[:, 'duration'] = np.where(df['start_date'] == df['end_date'],
                                     (df['end_time'] - df['start_time']),
                                     df['duration'])

    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)

    return df


def reset_steps_uno(df):
    '''Found this convenient, since removing and adding rows every function
       could lead to missing indexes and data not being in correct order.'''

    df.sort_values(by=['start_date', 'start_time'], inplace=True)
    df = df[df['num_steps'] > 0.4444].copy()
    df.loc[:, 'duration'] = np.where(df['start_date'] == df['end_date'],
                                     (df['end_time'] - df['start_time']),
                                     df['duration'])

    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    return df


def reset_steps_dos(df):
    '''Found this convenient, since removing and adding rows every function
       could lead to missing indexes and data not being in correct order.'''

    df.sort_values(by=['start_date', 'end_time'], inplace=True)
    df = df[df['num_steps'] > 0.4444].copy()
    df.loc[:, 'duration'] = np.where(df['start_date'] == df['end_date'],
                                     (df['end_time'] - df['start_time']),
                                     df['duration'])

    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    return df


def reset_floors_uno(df):
    '''Found this convenient, since removing and adding rows every function
       could lead to missing indexes and data not being in correct order.'''

    df.sort_values(by=['start_date', 'start_time'], inplace=True)
    df = df[df['num_floors'] > 0].copy()
    df.loc[:, 'duration'] = np.where(df['start_date'] == df['end_date'],
                                     (df['end_time'] - df['start_time']),
                                     df['duration'])

    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    return df


def reset_floors_dos(df):
    '''Found this convenient, since removing and adding rows every function
       could lead to missing indexes and data not being in correct order.'''

    df.sort_values(by=['start_date', 'end_time'], inplace=True)
    df = df[df['num_floors'] > 0].copy()
    df.loc[:, 'duration'] = np.where(df['start_date'] == df['end_date'],
                                     (df['end_time'] - df['start_time']),
                                     df['duration'])

    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    return df
