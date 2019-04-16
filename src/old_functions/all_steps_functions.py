# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd
from time import time


def clean_steps_data(soup):
    '''Step 1:
       Using Pandas to get a dataframe of all the values.'''

    tt = time()
    steps_df = pd.DataFrame()
    start_date_col = []
    end_date_col = []
    num_steps_col = []
    source_col = []

    steps = soup.findAll('Record',
                         {'type': 'HKQuantityTypeIdentifierStepCount'})

    for num in steps:
        start_date_col.append(num['startDate'])
        end_date_col.append(num['endDate'])
        num_steps_col.append(num['value'])
        source_col.append(num['sourceName'])

    steps_df.loc[:, 'start_date'] = start_date_col
    steps_df.loc[:, 'end_date'] = end_date_col
    steps_df.loc[:, 'num_steps'] = num_steps_col
    steps_df.loc[:, 'source'] = source_col

    steps_df.loc[:, 'num_steps'] = steps_df.num_steps.astype(int)

    steps_df.sort_values(by=['start_date', 'end_date'], inplace=True)
    steps_df = steps_df[steps_df['num_steps'] > 0.4444]
    steps_df.reset_index(inplace=True)
    steps_df.drop(columns=['index'], inplace=True)
    print(f'clean_steps_data {time()-tt}')

    return steps_df


def split_steps_between_days(df):
    '''Step : 4
       Split steps between days, in case a measurement starts on one day
       and finishes the following or more days from that time.'''

    i = 0
    tt = time()
    one_day = pd.Timedelta(1, unit='D')
    two_days = pd.Timedelta(2, unit='D')
    for i in range(len(df) - 1):
        if (df.end_date[i] - one_day) == df.start_date[i]:
            st_dt, st_tm, end_dt, end_tm, num_st, dur, sauce = df.iloc[i]
            ta = 24.0 - st_tm
            steps_per_hour = num_st / (end_tm + ta)

            num_st_1 = round(steps_per_hour * ta)
            num_st_2 = round(steps_per_hour * end_tm)

            df.loc[i+0.5] = [
                    end_dt, 0.0, end_dt, end_tm, num_st_2, end_tm, sauce]

            df.loc[i] = [
                    st_dt, st_tm, st_dt, 24.0, num_st_1, ta, sauce]

            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)

        elif (df.end_date[i] - two_days) == df.start_date[i]:
            st_dt, st_tm, end_dt, end_tm, num_st, dur, sauce = df.iloc[i]
            ta = 24.0 - st_tm

            steps_per_hour = num_st / (end_tm + 24.0 + ta)

            num_st_1 = round(steps_per_hour * ta)
            num_st_2 = round(steps_per_hour * 24.0)
            num_st_3 = round(steps_per_hour * end_tm)

            dt_2 = end_dt - one_day

            df.loc[i+0.1] = [dt_2, 0.0, dt_2, 24.0, num_st_2, 24.0, sauce]
            df.loc[i+0.2] = [end_dt, 0.0, end_dt,
                             end_tm, num_st_3, end_tm, sauce]
            df.loc[i] = [st_dt, st_tm, st_dt, 24.0, num_st_1, ta, sauce]

            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)
    print(f'split_steps_between_days {time()-tt}')
    return df


