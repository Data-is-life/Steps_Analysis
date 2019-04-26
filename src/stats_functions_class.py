# Author: Mohit Gangwani
# Date: 11/13/2018
# Git-Hub: Data-is-Life

import pandas as pd
import numpy as np
import re
from datetime import date, timedelta


class StatsHelper(object):
    """docstring for StatsHelper"""

    def __init__(self, dmyr):
        super(StatsHelper, self).__init__()
        self.dmyr = dmyr

    def split_str(self):
        '''The values for time period in the monthly and day of the week summarized
           df are combined. Using RegEx to split them.
           eg: Monday2017 to Monday 2017
               March2018  to March 2018'''

        nmyr = re.split(r'(\d+)', self.dmyr)
        dm = nmyr[0]
        yr = nmyr[1]
        return f'{dm} {yr}'

    def split_num(self):
        '''The values for time period in the day of the month summarized df are
           joined. Using RegEx to split them.
           eg: 012017 to 01-2017'''

        d_yr = re.split(r'(\d{2})', self.dmyr)
        d = d_yr[1]
        yr = d_yr[3] + d_yr[5]
        return f'{d}-{yr}'

    def weeks_dates(wky):
        '''The values for time period in the weekly summarized df are joined and
           in week numbers. Using RegEx and datetime to split them.
           eg: 432017 to "2017-10-23 to 2017-10-29"'''

        wk_yr = re.split(r'(\d{2})', wky)

        wk = int(wk_yr[1])
        yr = int(wk_yr[3] + wk_yr[5])
        d = date(yr, 1, 1)

        if(d.weekday() < 0):
            d -= timedelta(d.weekday())
        else:
            d += timedelta(6 - d.weekday())

        dlt = timedelta(days=(wk - 1) * 7)
        dts = f'{d + dlt} to {d + dlt + timedelta(days=6)}'
        return dts


class MainStats(object):
    '''This function is for summarizing df for desired time-frame.
       It returns the df sorted by the score for the specified time-frame.

       "dwm" is time-frame. It accepts the following strings:
       'Month', 'Week', 'Day of Week', or 'Day of Month'

       "s_by" is sort the by which score. It accepts the following strings:
       'steps', 'distance', or 'floors'
       '''

    def __init__(self, dwm, df, s_by='n/a'):
        super(MainStats, self).__init__()
        self.df = df
        self.dwm = dwm
        self.s_by = s_by
        self.meancols = ['mean_steps', 'mean_dist', 'mean_flrs', 'mean_fps']
        self.stdcols = ['std_steps', 'std_dist', 'std_flrs', 'std_fps']
        self.date_dict = {
            'week': ['%U%Y', 'week_range'], 'month': ['%B%Y', 'month_year'],
            'day of week': ['%A%Y', 'weekday_year'],
            'day of month': ['%d%Y', 'date_year']}
        self.sby_dict = {'steps': 'steps_score', 'distance': 'dist_score',
                         'floors': 'floors_score'}

    def custom_stats(self):
        date_ = self.date_dict[self.dwm][0]
        cols_ = self.date_dict[self.dwm][1]
        sort_ = self.sby_dict[self.s_by]
        std_df = self.df.groupby(df['start_date'].dt.strftime(date_),
                                 sort=False).std()
        std_df.columns = self.stdcols

        mean_df = self.df.groupby(self.df['start_date'].dt.strftime(date_),
                                  sort=False).mean()
        mean_df.columns = self.meancols

        score_df = pd.concat([std_df, mean_df], axis=1)
        score_df.reset_index(inplace=True)

        score_df.rename(columns={'start_date': cl_type}, inplace=True)
        score_df.loc[:, cl_type] = score_df[cl_type].apply(split_str_num)

        score_df.loc[:, 'steps_score'] = (score_df['mean_steps']**2) / score_df['std_steps']
        score_df.loc[:, 'dist_score'] = (score_df['mean_dist']**2) / score_df['std_dist']
        score_df.loc[:, 'floors_score'] = np.where(score_df['std_flrs'] >= 1e-4, ((score_df['mean_flrs']**2) / score_df['std_flrs']), 0)
        score_df.sort_values(by=sort_, ascending=False, inplace=True)

        score_df.reset_index(inplace=True)
        score_df.drop(columns=['index'], inplace=True)

        return score_df


class RollingStats(object):
    """docstring for RollingStats"""
    def __init__(self, df, x):
        super(RollingStats, self).__init__()
        self.x = x
        self.num_days = pd.Timedelta(self.x, unit='D')
        self.df = df[self.x:].copy()
        self.df.reset_index(inplace=True)
        self.df.drop(columns=['index', 'ft_per_step'], inplace=True)
        self.df.loc[:, 'start_date'] = self.df['end_date'] - self.num_days


    def drop_rename(self):
        '''This function is a real time saver. It trims the rows, drops
        unnecessary columns, renames columns based on the function, and sets
        index to start and end date. Otherwise, the following 13 lines would
        have to be re-entered after every operation.'''
        pass

    def rolling_stats(df, x):
        
        

def drop_change_rename_df(df, x, func_typ):
    
    

    

    df.rename(columns={'num_steps': func_typ + 'steps',
                       'tot_dist': func_typ + 'dist',
                       'num_floors': func_typ + 'floors'},
              inplace=True)

    df.set_index(['start_date', 'end_date'], inplace=True)

    return df



    '''I would like to rename this function later and call it the custom stat
       or something. This function does what iHealth won't do, which is give
       the user stats for any time-frame.
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
