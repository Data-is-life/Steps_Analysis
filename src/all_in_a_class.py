# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


class Fxyrs(object):
    '''docstring for ClassName'''
    def __init__(self, filename):
        self.filename = filename

    def first_clean(self):

        with open(self.file_name) as fp:
            soup = BeautifulSoup(fp, 'lxml-xml')

        flights = soup.findAll('Record',
                               {'type': 'HKQuantityTypeIdentifierFlightsClimbed'})
        distance = soup.findAll(
            'Record',
            {'type': 'HKQuantityTypeIdentifierDistanceWalkingRunning'})

        steps = soup.findAll('Record',
                             {'type': 'HKQuantityTypeIdentifierStepCount'})

        fdf = pd.DataFrame()
        sdf = pd.DataFrame()
        ddf = pd.DataFrame()

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
def trim_days(df, speed_unit, measure_unit):
    tt = time()
    one_day = pd.to_timedelta(1, 'D')
    two_days = pd.to_timedelta(2, 'D')
    df.loc[:, speed_unit] = df[measure_unit] / df['duration']
    for i in df.index:
        if df['start_date'][i] + one_day == df.end_date[i]:
            add_st = 0
            new_st = df.start_time[i]
            new_et = 24 - 1e-8
            add_et = df.end_time[i]
            new_dr = new_et - new_st
            add_dr = add_et
            speed  = df[speed_unit][i]
            new_td = speed * new_dr
            add_td = speed * add_dr
            new_sed = df['start_date'][i]
            add_sed = df['end_date'][i]
            src = df['source']
            df.loc[i, :] = [new_sed, new_sed, new_td, src, new_st, new_et,
                            new_dr, speed]
            df.loc[len(df), :] = [add_sed, add_sed, add_td, src, add_st,
                                  add_et, add_dr, speed]
            df.sort_values(by=['start_date', 'start_time', 'end_time'],
                            inplace=True)
            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)
        elif df['start_date'][i] + two_days == df.end_date[i]:
            new_st = df.start_time[i]
            add1_st, add2_st = 0, 0

            new_et, add1_et = 24 - 1e-8, 24 - 1e-8
            add2_et = df.end_time[i]

            new_dr = 24 - new_st
            add1_dr = 24
            add2_dr = add2_et

            speed  = df[speed_unit][i]

            new_td = speed * new_dr
            add1_td = speed * add1_dr
            add2_td = speed * add2_dr

            new_sed = df['start_date'][i]
            add1_sed = df['start_date'][i] + one_day
            add2_sed = df['end_date'][i]

            src = df['source']

            df.loc[i, :] = [new_sed, new_sed, new_td, src, new_st, new_et,
                            new_dr, speed]
            df.loc[len(df), :] = [add1_sed, add1_sed, add1_td, src, add1_st,
                                  add1_et, add1_dr, speed]
            df.loc[len(df) + 1, :] = [add2_sed, add2_sed, add2_td, src,
                                      add2_st, add2_et, add2_dr, speed]
            df.sort_values(by=['start_date', 'start_time', 'end_time'],
                            inplace=True)
            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)
    gc.collect()
    print(f'finished trim_days in {time()-tt}')
    return df