# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import gc
gc.enable()


def first_clean(file_name):

    # Step 1: Get data from xml using BeautifulSoup
    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'lxml-xml')

    '''Step 2: Parse all the flights climbed, distance walked, and steps taken
    data to a dictionary like format that makes it easy to extract values.'''
    flights = soup.findAll(
        'Record', {'type': 'HKQuantityTypeIdentifierFlightsClimbed'})
    distance = soup.findAll(
        'Record', {'type': 'HKQuantityTypeIdentifierDistanceWalkingRunning'})
    steps = soup.findAll(
        'Record', {'type': 'HKQuantityTypeIdentifierStepCount'})

    # Step 3: Create distance, steps, and flights dfs from the xml data.
    fdf = pd.DataFrame()
    sdf = pd.DataFrame()
    ddf = pd.DataFrame()

    # Using list comprehension to fill all the columns.
    fdf.loc[:, 'start_date'] = [num['startDate'] for num in flights]
    fdf.loc[:, 'end_date'] = [num['endDate'] for num in flights]
    fdf.loc[:, 'num_floors'] = [num['value'] for num in flights]
    fdf.loc[:, 'source'] = [num['sourceName'] for num in flights]
    fdf.loc[:, 'num_floors'] = fdf.num_floors.astype(int)

    sdf.loc[:, 'start_date'] = [num['startDate'] for num in steps]
    sdf.loc[:, 'end_date'] = [num['endDate'] for num in steps]
    sdf.loc[:, 'num_steps'] = [num['value'] for num in steps]
    sdf.loc[:, 'source'] = [num['sourceName'] for num in steps]
    sdf.loc[:, 'num_steps'] = sdf.num_steps.astype(int)

    ddf.loc[:, 'start_date'] = [num['startDate'] for num in distance]
    ddf.loc[:, 'end_date'] = [num['endDate'] for num in distance]
    ddf.loc[:, 'tot_dist'] = [num['value'] for num in distance]
    ddf.loc[:, 'source'] = [num['sourceName'] for num in distance]
    ddf.loc[:, 'tot_dist'] = ddf.tot_dist.astype(float)

    # Step 4: Sort values by date and time, and reset index.
    fdf.sort_values(by=['start_date', 'end_date'], inplace=True)
    sdf.sort_values(by=['start_date', 'end_date'], inplace=True)
    ddf.sort_values(by=['start_date', 'end_date'], inplace=True)

    fdf.reset_index(inplace=True)
    fdf.drop(columns=['index'], inplace=True)
    sdf.reset_index(inplace=True)
    sdf.drop(columns=['index'], inplace=True)
    ddf.reset_index(inplace=True)
    ddf.drop(columns=['index'], inplace=True)

    return sdf, ddf, fdf


def clean_start_end_times(df):

    '''Split start and end date, time, and timezone to a new df. Drop the
    Timezone column.'''
    start_date_df = df.start_date.str.split(
        ' ', expand=True).drop(columns=[2])
    end_date_df = df.end_date.str.split(' ', expand=True).drop(columns=[2])

    # Merge the start and end date & time to a single value.
    start_date_df.loc[:, 'std'] = start_date_df[0] + ' ' + start_date_df[1]
    end_date_df.loc[:, 'etd'] = end_date_df[0] + ' ' + end_date_df[1]

    # Convert the date to `datetime` and time to `timedelta`
    start_date_df.loc[:, 'sd'] = pd.to_datetime(
        start_date_df[0], format='%Y-%m-%d')
    end_date_df.loc[:, 'ed'] = pd.to_datetime(
        end_date_df[0], format='%Y-%m-%d')

    start_date_df.loc[:, 'st'] = pd.to_timedelta(start_date_df[1])
    end_date_df.loc[:, 'et'] = pd.to_timedelta(end_date_df[1])

    '''Insert the values in the original dataframe. Convert time to numerical
    format to make calculations easier.'''
    df.loc[:, 'start_date'] = start_date_df.sd.copy()
    df.loc[:, 'start_time'] = pd.to_numeric(start_date_df.st) / 3.6e12
    df.loc[:, 'end_date'] = end_date_df.ed.copy()
    df.loc[:, 'end_time'] = pd.to_numeric(end_date_df.et) / 3.6e12
    df.loc[:, 'duration'] = pd.to_numeric(
        (end_date_df.ed + end_date_df.et) - (
            start_date_df.sd + start_date_df.st)) / 3.6e12

    gc.collect()
    return df

def trim_one_day(df, speed_unit, measure_unit):

    # Create a variable for one day and a unit to measure speed.
    one_day = pd.to_timedelta(1, 'D')
    df.loc[:, speed_unit] = df[measure_unit] / df['duration']

    # Create two different dfs to do separate calculations.
    ndf1 = df[df['start_date'] + one_day == df['end_date']].copy()
    ndf2 = df[df['start_date'] + one_day == df['end_date']].copy()

    '''Calculations for the first data frame are to trim values till the end
    of the first day. The calculations are done as follow:
       1. End date is the start date
       2. End time is 23.9999999999999999999
       3. Duration is from starting time till midnight
       4. the `measure_unit` is calculated by multiplying the `speed_unit` and
          the new calculated duration.
       5. Reset the index'''
    ndf1.loc[:, 'end_date'] = ndf1['start_date'].copy()
    ndf1.loc[:, 'end_time'] = 24 - 1e-10
    ndf1.loc[:, 'duration'] = ndf1['end_time'] - ndf1['start_time']
    ndf1.loc[:, measure_unit] = ndf1[speed_unit] * ndf1['duration']
    ndf1.reset_index(inplace=True)
    ndf1.drop(columns=['index'], inplace=True)

    '''Calculations for the second df are to trim values starting at midnight
    of the following day. The calculations are done as follow:
       1. Start date is the end date
       2. Start time is 0.0
       3. Duration is from midnight till the ending time  
       4. the `measure_unit` is calculated by multiplying the `speed_unit` and
          the new calculated duration.
       5. Reset the index'''
    ndf2.loc[:, 'start_date'] = ndf2['end_date'].copy()
    ndf2.loc[:, 'start_time'] = 0.0
    ndf2.loc[:, 'duration'] = ndf2['end_time'] - ndf2['start_time']
    ndf2.loc[:, measure_unit] = ndf2[speed_unit] * ndf2['duration']
    ndf2.reset_index(inplace=True)
    ndf2.drop(columns=['index'], inplace=True)

    '''Drop the rows where the data spills to the next day, and append the
    new calculated values'''
    df = df[df['start_date'] + one_day != df['end_date']].copy()
    df = df.append([ndf1, ndf2], ignore_index=True, sort=False)
    df.sort_values(by=['start_date', 'start_time', 'end_time'], inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)

    return df


def trim_two_days(df, speed_unit, measure_unit):
    # Create a variable for one day, two days and a unit to measure speed.
    one_day = pd.to_timedelta(1, 'D')
    two_days = pd.to_timedelta(2, 'D')
    df.loc[:, speed_unit] = df[measure_unit] / df['duration']

    # Create three different dfs to do separate calculations.
    ndf1 = df[df['start_date'] + two_days == df['end_date']].copy()
    ndf2 = df[df['start_date'] + two_days == df['end_date']].copy()
    ndf3 = df[df['start_date'] + two_days == df['end_date']].copy()

    '''Calculations for the first data frame are to trim values till the end
    of the first day. The calculations are done as follow:
       1. End date is the start date
       2. End time is 23.9999999999999999999
       3. Duration is from starting time till midnight
       4. the `measure_unit` is calculated by multiplying the `speed_unit` and
          the new calculated duration.
       5. Reset the index'''
    ndf1.loc[:, 'end_date'] = ndf1['start_date'].copy()
    ndf1.loc[:, 'end_time'] = 24 - 1e-10
    ndf1.loc[:, 'duration'] = (24 - 1e-10) - ndf1['start_time']
    ndf1.loc[:, measure_unit] = ndf1[speed_unit] * ndf1['duration']
    ndf1.reset_index(inplace=True)
    ndf1.drop(columns=['index'], inplace=True)

    '''Calculations for the second data frame are to trim values till the end
    of the first day. The calculations are done as follow:
       1. End date and start date are one day after the starting date
       2. Start time is 0.0
       2. End time is 23.9999999999999999999
       3. Duration is 24 hours
       4. the `measure_unit` is calculated by multiplying the `speed_unit` and
          the new calculated duration = 24 hours.
       5. Reset the index'''
    ndf2.loc[:, 'start_date'] = ndf2['start_date'] + one_day
    ndf2.loc[:, 'end_date'] = ndf2['start_date'] + one_day
    ndf2.loc[:, 'start_time'] = 0
    ndf1.loc[:, 'end_time'] = 24 - 1e-10
    ndf2.loc[:, 'duration'] = 24 - 1e-10
    ndf2.loc[:, measure_unit] = ndf2[speed_unit] * (24 - 1e-10)
    ndf2.reset_index(inplace=True)
    ndf2.drop(columns=['index'], inplace=True)

    '''Calculations for the third df are to trim values starting at midnight
    of the last day. The calculations are done as follow:
       1. Start date is the end date
       2. Start time is 0.0
       3. Duration is from midnight till the ending time  
       4. the `measure_unit` is calculated by multiplying the `speed_unit` and
          the new calculated duration.
       5. Reset the index'''
    ndf3.loc[:, 'start_date'] = ndf3['end_date'].copy()
    ndf3.loc[:, 'start_time'] = 0
    ndf3.loc[:, 'duration'] = ndf3['end_time'].copy()
    ndf3.loc[:, measure_unit] = ndf3[speed_unit] * ndf3['duration']
    ndf3.reset_index(inplace=True)
    ndf3.drop(columns=['index'], inplace=True)

    '''Drop the rows where the data spills to two days, and append the
    new calculated values'''
    df = df[df['start_date'] + two_days != df['end_date']].copy()
    df = df.append([ndf1, ndf2, ndf3], ignore_index=True, sort=False)
    df.sort_values(by=['start_date', 'start_time', 'end_time'], inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)

    return df


def remove_overlapping_rows(df):
    '''Creating three conditions:
       1. The start time of the row has to be greater than the start time of
          the next row.
       2. The end time of the row has to be less than the end time of the
          next row.
       3. The start date of the row has to be same than the start date of
          the next row.
        If all conditions match, the row is dropped, since we already had data
        for that time.'''
    ldf = len(df)
    pdf = 0
    while ldf != pdf:
        ldf = len(df)
        df.loc[:, 'cond1'] = np.where(
            df.start_time >= df.start_time.shift(1), 1, 0)
        df.loc[:, 'cond2'] = np.where(
            df.end_time <= df.end_time.shift(1), 1, 0)
        df.loc[:, 'cond3'] = np.where(
            df.start_date == df.start_date.shift(1), 1, 0)

        df.loc[:, 'condsum'] = df.cond1 + df.cond2 + df.cond3
        df = df[df['condsum'] < 3].copy()
        pdf = len(df)

    gc.collect()
    df.reset_index(inplace=True)
    df.drop(columns=['cond1', 'cond2', 'cond3', 'condsum', 'index'],
             inplace=True)
    return df


def trim_data(df, speed_unit, measure_unit):
    '''Creating three conditions:
       1. The end time of the row has to be greater than the start time of
          the next row.
       2. The start date of the row has to be same than the start date of
          the next row.
       3. The sources have to be different, otherwise, we are just grouping
          all the data.'''
    df.loc[:, 'cond1'] = np.where(df.end_time >= df.start_time.shift(1), 1, 0)
    df.loc[:, 'cond2'] = np.where(
        df.start_date == df.start_date.shift(1), 1, 0)
    df.loc[:, 'conds'] = np.where(df.source != df.source.shift(1), 1, 0)
    df.loc[:, 'condsum'] = df.cond1 + df.cond2 + df.conds
    df.drop(columns=['cond1', 'cond2', 'conds'], inplace=True)

    # Duration is recalculated to make sure it is right.
    df.loc[:, 'duration'] = df.end_time - df.start_time

    '''Data is trimmed from a row if all the conditions match. Following
       calculations are performed if all the conditions match.:
       1. The start time of the row is the end time of the previous row.
       2. Duration is recalculated.
       3. `measure_unit` is recalculated by multiplying the new duration
          and the `speed_unit`.'''
    df.loc[:, 'start_time'] = np.where(
        df['condsum'] == 3, df.end_time.shift(1) - 1e-10, df.start_time)
    df.loc[:, 'duration'] = np.where(
        df['condsum'] == 3, df.end_time - df.start_time, df['duration'])
    df.loc[:, measure_unit] =  np.where(
        df['condsum'] == 3, df.duration * df[speed_unit], df[measure_unit])

    df.reset_index(inplace=True)
    df.drop(columns=['index', 'condsum'], inplace=True)
    return df


def main_func(file_name):
    sdf, ddf, fdf = first_clean(file_name)
    fdf = clean_start_end_times(fdf)
    ddf = clean_start_end_times(ddf)
    sdf = clean_start_end_times(sdf)

    fdf = trim_one_day(fdf, 'fph', 'num_floors')
    sdf = trim_one_day(sdf, 'sph', 'num_steps')
    ddf = trim_one_day(ddf, 'mph', 'tot_dist')

    fdf = trim_two_days(fdf, 'fph', 'num_floors')
    sdf = trim_two_days(sdf, 'sph', 'num_steps')
    ddf = trim_two_days(ddf, 'mph', 'tot_dist')

    fdf = remove_overlapping_rows(fdf)
    sdf = remove_overlapping_rows(sdf)
    ddf = remove_overlapping_rows(ddf)

    fdf = trim_data(fdf, 'fph', 'num_floors')
    sdf = trim_data(sdf, 'sph', 'num_steps')
    ddf = trim_data(ddf, 'mph', 'tot_dist')

    sdf.drop(columns=['start_time', 'end_time', 'duration'], inplace=True)
    ddf.drop(columns=['start_time', 'end_time', 'duration'], inplace=True)
    fdf.drop(columns=['start_time', 'end_time', 'duration'], inplace=True)

    dsdf = sdf.groupby(by=['start_date', 'end_date']).sum()
    dddf = ddf.groupby(by=['start_date', 'end_date']).sum()
    dfdf = fdf.groupby(by=['start_date', 'end_date']).sum()
    gc.collect()

    cdf = pd.concat([dsdf, dddf, dfdf], sort=False, axis=1)

    cdf.loc[:, 'ft_per_step'] = cdf.tot_dist * 5280 / cdf.num_steps
    cdf.drop(columns=['sph', 'mph', 'fph'], inplace=True)

    cdf.reset_index(inplace=True)
    cdf.fillna(0, inplace=True)

    return fdf, ddf, sdf, cdf
