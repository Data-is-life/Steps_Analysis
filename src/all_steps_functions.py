# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd


def clean_steps_data(soup):
    '''Step 1:
       Using Pandas to get a dataframe of all the values.'''

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

    return steps_df


def split_steps_between_days(df):
    '''Step : 4
       Split steps between days, in case a measurement starts on one day
       and finishes the following or more days from that time.'''

    i = 0
    for i in range(len(df) - 1):

        if (df.end_date[i] - pd.Timedelta(1, unit='D') == df.start_date[i]):

            st_dt, st_tm, end_dt, end_tm, num_st, dur, sauce = df.iloc[i]

            steps_per_hour = num_st / (end_tm + (24.0 - st_tm))

            num_st_1 = round(steps_per_hour * (24.0 - st_tm))
            num_st_2 = round(steps_per_hour * end_tm)

            df.loc[i + .1] = [end_dt, 0.0, end_dt, end_tm,
                              num_st_2, end_tm, sauce]

            df.loc[i] = [st_dt, st_tm, st_dt, 24.0,
                         num_st_1, (24.0 - st_tm), sauce]

            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)

        elif (df.end_date[i] - pd.Timedelta(2, unit='D') == df.start_date[i]):

            st_dt, st_tm, end_dt, end_tm, num_st, dur, sauce = df.iloc[i]
            steps_per_hour = num_st / (end_tm + 24.0 + (24.0 - st_tm))

            num_st_1 = round(steps_per_hour * (24.0 - st_tm))
            num_st_2 = round(steps_per_hour * 24.0)
            num_st_3 = round(steps_per_hour * end_tm)

            dt_2 = end_dt - pd.Timedelta(1, unit='D')

            df.loc[i + .1] = [dt_2, 0.0, dt_2, 24.0,
                              num_st_2, 24.0, sauce]
            df.loc[i + .2] = [end_dt, 0.0, end_dt, end_tm,
                              num_st_3, end_tm, sauce]
            df.loc[i] = [st_dt, st_tm, st_dt, 24.0,
                         num_st_1, (24.0 - st_tm), sauce]

            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)

    return df


def trim_steps_from_overlapping_times(df):
    '''Step : 6
       Correct total steps and times from overlapping times.

       To trim steps, make sure to check if start date for the same row are
       the same and make sure the following row has the same starting and
       ending date.

       Also, the starting time of the following row has to be less than ending
       time for the row to check and the ending time for the following row has
       to be greater.

       Once the steps are trimmed, if the remaining steps are less than
       0.4444, drop the row.

       Rounding 0.4444 to an integer will be 0.'''

    i = 0
    while i < len(df) - 1:
        if (df.start_date[i] == df.end_date[i]) and (
                df.start_date[i] == df.end_date[i + 1]) and(
                df.start_date[i] == df.start_date[i + 1]) and (
                df.start_time[i + 1] <= df.end_time[i]) and (
                df.end_time[i + 1] >= df.end_time[i]):

            steps_per_hour = df.num_steps[
                i + 1] / (df.end_time[i + 1] - df.start_time[i + 1])

            steps_adjust = (df.end_time[i] -
                            df.start_time[i + 1]) * steps_per_hour

            steps_adjust = round(steps_adjust)

            df.loc[(i + 1), 'num_steps'] = df.num_steps[i + 1] - steps_adjust
            df.loc[(i + 1), 'start_time'] = df.end_time[i]
            df.loc[(i + 1), 'duration'] = df.end_time[i + 1] - \
                df.start_time[i + 1]

            df.loc[i, 'duration'] = df.end_time[i] - df.start_time[i]

            if df.num_steps[i + 1] < 0.4444:
                df.drop(index=(i + 1), inplace=True)
                df.reset_index(inplace=True)
                df.drop(columns=['index'], inplace=True)
            else:
                i += 1

        else:
            i += 1

    return df
