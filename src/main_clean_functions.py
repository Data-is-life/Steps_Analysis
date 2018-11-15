# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd
from bs4 import BeautifulSoup

from all_distance_functions import clean_distance_data
from all_distance_functions import split_distance_between_days
from all_distance_functions import trim_distance_from_overlapping_times

from all_steps_functions import clean_steps_data
from all_steps_functions import split_steps_between_days
from all_steps_functions import trim_steps_from_overlapping_times

from all_flights_climbed_functions import clean_flights_data
from all_flights_climbed_functions import split_num_flights_between_days
from all_flights_climbed_functions import trim_flights_climbed_from_overlapping_times

from common_cleaning_functions import clean_duration
from common_cleaning_functions import clean_columns_conv_to_numeric
from common_cleaning_functions import remove_overlap_time_rows
from common_cleaning_functions import reset_distance_uno
from common_cleaning_functions import reset_distance_dos
from common_cleaning_functions import reset_steps_uno
from common_cleaning_functions import reset_steps_dos
from common_cleaning_functions import reset_floors_uno
from common_cleaning_functions import reset_floors_dos


def main_clean_function(file_name):
    '''This function takes all ther other functions and cleans distance, steps,
       and the number of flights climbed from the xml file.'''

    # Step 1: Get data from xml using BeautifulSoup
    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'lxml-xml')

    # Step 2: Create distance, steps, and flights climbed dfs from the xml data
    steps_df = clean_steps_data(soup)
    dist_df = clean_distance_data(soup)
    floors_df = clean_flights_data(soup)

    # Step 3: create a new dfs to clean values
    dur_stp_df = clean_duration(steps_df)
    dur_dst_df = clean_duration(dist_df)
    dur_flt_df = clean_duration(floors_df)

    '''Step 4: combine df created from xml and duration df, remove unnecessary
       columns, convert time and duration to numeric'''
    stp_df, dst_df, flr_df = clean_columns_conv_to_numeric(
        steps_df, dist_df, floors_df, dur_stp_df, dur_dst_df, dur_flt_df)

    # Step 5: split multi-day data.
    stp_df = split_steps_between_days(stp_df)
    dst_df = split_distance_between_days(dst_df)
    flr_df = split_distance_between_days(flr_df)

    stp_df = reset_steps_uno(stp_df)
    dst_df = reset_distance_uno(dst_df)
    dst_df = reset_distance_dos(dst_df)
    flr_df = reset_floors_uno(flr_df)

    # Step 6: remove overlapping times rows.
    stp_df = remove_overlap_time_rows(stp_df)
    dst_df = remove_overlap_time_rows(dst_df)
    flr_df = remove_overlap_time_rows(flr_df)

    stp_df = reset_steps_uno(stp_df)
    dst_df = reset_distance_uno(dst_df)
    dst_df = reset_distance_dos(dst_df)
    flr_df = reset_floors_uno(flr_df)

    # Step 7: trim steps and distance from overlapping times.
    stp_df = trim_steps_from_overlapping_times(stp_df)
    dst_df = trim_distance_from_overlapping_times(dst_df)
    flr_df = trim_flights_climbed_from_overlapping_times(flr_df)

    stp_df = reset_steps_uno(stp_df)
    dst_df = reset_distance_uno(dst_df)
    dst_df = reset_distance_dos(dst_df)
    flr_df = reset_floors_uno(flr_df)

    stp_df = stp_df[stp_df['duration'] > 1.0e-5]
    dst_df = dst_df[dst_df['duration'] > 1.0e-5]

    stp_df = reset_steps_dos(stp_df)
    stp_df = reset_steps_uno(stp_df)
    dst_df = reset_distance_uno(dst_df)
    dst_df = reset_distance_dos(dst_df)
    flr_df = reset_floors_dos(flr_df)
    flr_df = reset_floors_uno(flr_df)

    stp_df.drop(columns=['start_time', 'end_time', 'duration'], inplace=True)
    dst_df.drop(columns=['start_time', 'end_time', 'duration'], inplace=True)
    flr_df.drop(columns=['start_time', 'end_time', 'duration'], inplace=True)

    return stp_df, dst_df, flr_df


def create_combined_daily_df(stp_df, dst_df, flr_df):
    '''To run stats, first thing to do is get total for each day.
       So, group it by start and end date, they should be the same
       Also, added a column feet/steps'''

    daily_stp_df = stp_df.groupby(by=['start_date', 'end_date']).sum()
    daily_dst_df = dst_df.groupby(by=['start_date', 'end_date']).sum()
    daily_flr_df = flr_df.groupby(by=['start_date', 'end_date']).sum()

    cmb_df = pd.concat([daily_stp_df, daily_dst_df,
                        daily_flr_df], sort=False, axis=1)

    cmb_df.loc[:, 'ft_per_step'] = cmb_df.tot_dist * 5280 / cmb_df.num_steps

    cmb_df.reset_index(inplace=True)
    cmb_df.num_floors.fillna(0, inplace=True)

    return cmb_df
