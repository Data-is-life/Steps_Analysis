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

    nmy = re.split('(\d+)', dmyr)
    dm = nmyr[0]
    yr = nmyr[1]
    return dm + ' ' + yr


def split_num_num(dyr):
    '''The values for time period in the day of the month summarized df are
       joined. Using RegEx to split them.
       eg: 012017 to 01-2017'''

    d_yr = re.split('(\d{2})', wky)
    d = d_yr[1]
    yr = d_yr[3] + d_yr[5]
    return d + '-' + yr


def get_weeks_dates(wky):
    '''The values for time period in the weekly summarized df are joined and
       in week numbers. Using RegEx and datetime to split them.
       eg: 432017 to "2017-10-23 to 2017-10-29"'''

    wk_yr = re.split('(\d{2})', wky)

    wk = int(wk_yr[1])
    yr = int(wk_yr[3] + wk_yr[5])

    d = date(yr, 1, 1)

    if(d.weekday() <= 3):
        d = d - timedelta(d.weekday())

    else:
        d = d + timedelta(7 - d.weekday())

    dlt = timedelta(days=(wk - 1) * 7)

    dts = f'{d + dlt} to {d + dlt + timedelta(days=6)}'
    return dts


def get_stats_day_week_month(df, dwm):
    '''This function is for summarizing df for desired timeframe.
       It returns the df sorted by the score for the specified timeframe.

       It accepts the following time frames:
       Month
       Week
       Day of Week
       Day of Month'''

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

    score_df.loc[:, 'score'] = score_df['mean_stp'] / score_df['std_stp']
    score_df.sort_values(by='score', ascending=False, inplace=True)

    return score_df


def drop_change_rename_df(df, x, func_typ):

    df.drop(df.index[list(range(x - 1))], inplace=True)
    df.reset_index(inplace=True)
#     df.drop(columns=['index'], inplace=True)
    df.loc[:, 'start_date'] = df['end_date'] - pd.Timedelta(x, unit='D')
    df.rename(columns={'num_steps': func_typ + 'num_steps'}, inplace=True)
    if 'index' in df.columns:
        df.drop(columns=['index'], inplace=True)
    df.set_index(['start_date', 'end_date'], inplace=True)

    return df


def rolling_day_df(df, x):
    df.set_index(['start_date', 'end_date'], inplace=True)

    m_df = df.rolling(x).mean()
    m_df.reset_index(inplace=True)

    md_df = df.rolling(x).median()
    md_df.reset_index(inplace=True)

    std_df = df.rolling(x).std()
    std_df.reset_index(inplace=True)

    s_df = df.rolling(x).sum()
    s_df.reset_index(inplace=True)

    min_df = df.rolling(x).min()
    min_df.reset_index(inplace=True)

    max_df = df.rolling(x).max()
    max_df.reset_index(inplace=True)

    m_df = drop_change_rename_df(m_df, x, 'mean_')
    md_df = drop_change_rename_df(md_df, x, 'median_')
    merged_df_uno = pd.merge(m_df, md_df, on=m_df.index)

    std_df = drop_change_rename_df(std_df, x, 'std_')
    s_df = drop_change_rename_df(s_df, x, 'total_')
    merged_df_dos = pd.merge(std_df, s_df, on=std_df.index)

    min_df = drop_change_rename_df(min_df, x, 'min_')
    max_df = drop_change_rename_df(max_df, x, 'max_')
    merged_df_tres = pd.merge(min_df, max_df, on=min_df.index)

    merged_df_quatro = pd.merge(merged_df_uno, merged_df_dos,
                                on=merged_df_uno.index)

    merged_df_finale = pd.merge(merged_df_quatro, merged_df_tres,
                                on=merged_df_tres.index)

    merged_df_finale.drop(columns=['key_0_y'], inplace=True)

    merged_df_finale['steps_score_mean'] = merged_df_finale['mean_num_steps'] / \
        merged_df_finale['std_num_steps']

    merged_df_finale['steps_score_median'] = merged_df_finale['median_num_steps'] / \
        merged_df_finale['std_num_steps']

    merged_df_finale.reset_index(inplace=True)

    merged_df_finale.drop(columns=['index', 'key_0'], inplace=True)

    return merged_df_finale
