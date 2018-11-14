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

from common_cleaning_functions import clean_duration
from common_cleaning_functions import clean_columns_conv_to_numeric
from common_cleaning_functions import remove_overlap_time_rows
from common_cleaning_functions import reset_distance_uno
from common_cleaning_functions import reset_distance_dos
from common_cleaning_functions import reset_steps_uno
from common_cleaning_functions import reset_steps_dos


def main_clean_function(file_name):
    '''This function takes all ther other functions and cleans distance
       and steps from the xml file.'''

    # Step 1: Get data from xml using BeautifulSoup
    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'lxml-xml')

    # Step 2: create distance and steps dataframes from xml data
    steps_df = clean_steps_data(soup)
    dist_df = clean_distance_data(soup)

    # Step 3: create a new dfs to clean values
    dur_stp_df = clean_duration(steps_df)
    dur_dst_df = clean_duration(dist_df)

    '''Step 4: combine df created from xml and duration df, remove unnecessary
    columns, convert time and duration to numeric'''
    stp_df, dst_df = clean_columns_conv_to_numeric(
        steps_df, dist_df, dur_stp_df, dur_dst_df)

    # Step 5: split multi-day data.
    stp_df = split_steps_between_days(stp_df)
    dst_df = split_distance_between_days(dst_df)

    stp_df = reset_steps_uno(stp_df)
    dst_df = reset_distance_uno(dst_df)
    dst_df = reset_distance_dos(dst_df)

    # Step 6: remove overlapping times rows.
    stp_df = remove_overlap_time_rows(stp_df)
    dst_df = remove_overlap_time_rows(dst_df)

    stp_df = reset_steps_uno(stp_df)
    dst_df = reset_distance_uno(dst_df)
    dst_df = reset_distance_dos(dst_df)

    # Step 7: trim steps and distance from overlapping times.
    stp_df = trim_steps_from_overlapping_times(stp_df)
    dst_df = trim_distance_from_overlapping_times(dst_df)
    stp_df = reset_steps_uno(stp_df)
    dst_df = reset_distance_uno(dst_df)
    dst_df = reset_distance_dos(dst_df)

    stp_df = stp_df[stp_df['duration'] > 1.0e-5]
    dst_df = dst_df[dst_df['duration'] > 1.0e-5]

    stp_df = reset_steps_dos(stp_df)
    stp_df = reset_steps_uno(stp_df)
    dst_df = reset_distance_uno(dst_df)
    dst_df = reset_distance_dos(dst_df)

    return stp_df, dst_df


def create_combined_daily_df(stp_df, dst_df):
    '''To run stats, first thing to do is get total for each day.
       So, group it by start and end date, they should be the same
       get rid of start_time, end_time, and duration columns.'''

    stp_df.drop(columns=['start_time', 'end_time', 'duration'], inplace=True)
    dst_df.drop(columns=['start_time', 'end_time', 'duration'], inplace=True)

    daily_stp_df = stp_df.groupby(by=['start_date', 'end_date']).sum()
    daily_dst_df = dst_df.groupby(by=['start_date', 'end_date']).sum()

    daily_stp_df.reset_index(inplace=True)
    daily_dst_df.reset_index(inplace=True)

    combined_df = pd.concat([daily_stp_df, daily_dst_df], sort=False, axis=1)

    return combined_df
