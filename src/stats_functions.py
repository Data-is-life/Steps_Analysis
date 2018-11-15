# Author: Mohit Gangwani
# Date: 11/13/2018
# Git-Hub: Data-is-Life

import pandas as pd
import re
from datetime import date, timedelta


def split_str_num(dmyr):
    '''The values for time period in the monthly and day of the week summarized
       df are combined. Using RegEx to split them.
       eg: Monday2017 to Monday 2017
           March2018  to March 2018'''

    nmyr = re.split(r'(\d+)', dmyr)
    dm = nmyr[0]
    yr = nmyr[1]
    return dm + ' ' + yr


def split_num_num(dyr):
    '''The values for time period in the day of the month summarized df are
       joined. Using RegEx to split them.
       eg: 012017 to 01-2017'''

    d_yr = re.split(r'(\d{2})', dyr)
    d = d_yr[1]
    yr = d_yr[3] + d_yr[5]
    return d + '-' + yr


def get_weeks_dates(wky):
    '''The values for time period in the weekly summarized df are joined and
       in week numbers. Using RegEx and datetime to split them.
       eg: 432017 to "2017-10-23 to 2017-10-29"'''

    wk_yr = re.split(r'(\d{2})', wky)

    wk = int(wk_yr[1])
    yr = int(wk_yr[3] + wk_yr[5])

    d = date(yr, 1, 1)

    if(d.weekday() < 0):
        d = d - timedelta(d.weekday())

    else:
        d = d + timedelta(6 - d.weekday())

    dlt = timedelta(days=(wk - 1) * 7)

    dts = f'{d + dlt} to {d + dlt + timedelta(days=6)}'
    return dts


def get_stats_day_week_month(df, dwm='n/a', s_by='n/a'):
    '''This function is for summarizing df for desired timeframe.
       It returns the df sorted by the score for the specified timeframe.

       "dwm" is timeframe. It accepts the following strings:
       'Month', 'Week', 'Day of Week', or 'Day of Month'

       "s_by" is sort the by which score. It accepts the following strings:
       'steps' or 'distance'
       '''

    if dwm.lower() == 'month':
        std_df = df.groupby(df['start_date'].dt.strftime('%B%Y'),
                            sort=False).std()
        std_df.columns = ['std_steps', 'std_dist', 'std_fps']

        mean_df = df.groupby(df['start_date'].dt.strftime('%B%Y'),
                             sort=False).mean()
        mean_df.columns = ['mean_steps', 'mean_dist', 'mean_fps']

        score_df = pd.concat([std_df, mean_df], axis=1)
        score_df.reset_index(inplace=True)

        score_df.rename(columns={'start_date': 'month_year'}, inplace=True)

        score_df.loc[:, 'month_year'] = score_df.month_year.apply(
            split_str_num)

    elif dwm.lower() == 'day of week':
        std_df = df.groupby(df['start_date'].dt.strftime('%A%Y'),
                            sort=False).std()
        std_df.columns = ['std_steps', 'std_dist', 'std_fps']

        mean_df = df.groupby(df['start_date'].dt.strftime('%A%Y'),
                             sort=False).mean()
        mean_df.columns = ['mean_steps', 'mean_dist', 'mean_fps']

        score_df = pd.concat([std_df, mean_df], axis=1)
        score_df.reset_index(inplace=True)

        score_df.rename(columns={'start_date': 'weekday_year'}, inplace=True)

        score_df.loc[:, 'weekday_year'] = score_df.weekday_year.apply(
            split_str_num)

    elif dwm.lower() == 'day of month':
        std_df = df.groupby(df['start_date'].dt.strftime('%d%Y'),
                            sort=False).std()
        std_df.columns = ['std_steps', 'std_dist', 'std_fps']

        mean_df = df.groupby(df['start_date'].dt.strftime('%d%Y'),
                             sort=False).mean()
        mean_df.columns = ['mean_steps', 'mean_dist', 'mean_fps']

        score_df = pd.concat([std_df, mean_df], axis=1)
        score_df.reset_index(inplace=True)

        score_df.rename(columns={'start_date': 'date_year'}, inplace=True)

        score_df.loc[:, 'date_year'] = score_df.date_year.apply(split_num_num)

    elif dwm.lower() == 'week':
        std_df = df.groupby(df['start_date'].dt.strftime('%U%Y'),
                            sort=False).std()
        std_df.columns = ['std_steps', 'std_dist', 'std_fps']

        mean_df = df.groupby(df['start_date'].dt.strftime('%U%Y'),
                             sort=False).mean()
        mean_df.columns = ['mean_steps', 'mean_dist', 'mean_fps']

        score_df = pd.concat([std_df, mean_df], axis=1)
        score_df.reset_index(inplace=True)

        score_df.rename(columns={'start_date': 'week_range'}, inplace=True)

        score_df.loc[:, 'week_range'] = score_df.week_range.apply(
            get_weeks_dates)

    else:
        return 'Please enter "month", "week", "day of week", or "day of month"'

    score_df.loc[:, 'steps_score'] = (score_df[
        'mean_steps']**2) / score_df['std_steps']
    score_df.loc[:, 'dist_score'] = score_df[
        'mean_dist'] / score_df['std_dist']

    if s_by.lower() == 'steps':
        score_df.sort_values(by='steps_score', ascending=False, inplace=True)

    elif s_by.lower() == 'distance':
        score_df.sort_values(by='dist_score', ascending=False, inplace=True)

    else:
        return 'Please enter "steps" or "distance"'

    score_df.reset_index(inplace=True)
    score_df.drop(columns=['index'], inplace=True)

    return score_df


def drop_change_rename_df(df, x, func_typ):
    '''This function is a real timesaver. It trims the rows, drops columns
       not needed, renames columns based on the function, and sets index
       to start and end date. Otherwise, the following 13 lines would have
       to be re-entered after every operation. :)''' 

    df = df[x:].copy()
    df.reset_index(inplace=True)
    df.drop(columns=['index', 'ft_per_step'], inplace=True)

    df.loc[:, 'start_date'] = df[
        'end_date'] - pd.Timedelta(x, unit='D')

    df.rename(columns={'num_steps': func_typ + 'num_steps',
                       'tot_dist': func_typ + 'tot_dist'},inplace=True)

    df.set_index(['start_date', 'end_date'], inplace=True)    

    return df


def rolling_day_df(df, x):
    '''I would like to rename this function later and call it the custom stat
       or something. This function does what iHealth won't do, which is give
       the user stats for any timeframe.
       x is the number of days of rolling stats.''' 

    df.set_index(['start_date', 'end_date'], inplace=True)

    mean_df = df.rolling(x).mean()
    mean_df.reset_index(inplace=True)
    mean_df = drop_change_rename_df(mean_df, x, 'mean_')

    median_df = df.rolling(x).median()
    median_df.reset_index(inplace=True)
    median_df = drop_change_rename_df(median_df, x, 'median_')

    std_df = df.rolling(x).std()
    std_df.reset_index(inplace=True)
    std_df = drop_change_rename_df(std_df, x, 'std_')

    sum_df = df.rolling(x).sum()
    sum_df.reset_index(inplace=True)
    sum_df = drop_change_rename_df(sum_df, x, 'total_')

    min_df = df.rolling(x).min()
    min_df.reset_index(inplace=True)
    min_df = drop_change_rename_df(min_df, x, 'min_')

    max_df = df.rolling(x).max()
    max_df.reset_index(inplace=True)
    max_df = drop_change_rename_df(max_df, x, 'max_')

    merged_df = pd.concat([mean_df, median_df, std_df,
                           sum_df, min_df, max_df], axis=1)

    merged_df.reset_index(inplace=True)

    df.reset_index(inplace=True)

    return merged_df
