# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd

from all_distance_functions import clean_distance_data
from all_distance_functions import split_distance_between_days
from all_distance_functions import trim_distance_from_overlapping_times

from all_steps_functions import clean_steps_data
from all_steps_functions import split_steps_between_days
from all_steps_functions import trim_steps_from_overlapping_times

from common_cleaning_functions import clean_duration
from common_cleaning_functions import remove_overlap_time_rows
from common_cleaning_functions import reset_distance_uno
from common_cleaning_functions import reset_distance_dos
from common_cleaning_functions import reset_steps_uno
from common_cleaning_functions import reset_steps_dos


def steps_clean_function(soup):
    '''This function takes all ther other functions and puts it together.'''

    steps_df = clean_steps_data(soup)  # Step 1: create a df from xml data

    # Step 2: create a new df to clean values
    dur_df = clean_duration(steps_df)

    steps_df.drop(columns=['start_date', 'end_date'], inplace=True)

    # Step 3: xml input file all parsed
    df = pd.concat([steps_df, dur_df], axis=1)

    df = df[['start_date', 'start_time', 'end_date',
             'end_time', 'num_steps', 'duration', 'source']]

    df = reset_steps_uno(df)

    '''I found working with numbers easier than working with Timedeltas'''
    df.loc[:, 'start_time'] = pd.to_numeric(df['start_time']) / 3600000000000
    df.loc[:, 'end_time'] = pd.to_numeric(df['end_time']) / 3600000000000
    df.loc[:, 'duration'] = pd.to_numeric(df['duration']) / 3600000000000

    df = split_steps_between_days(df)  # Step 4: split multi-day data.

    df = reset_steps_uno(df)

    df = remove_overlap_time_rows(df)  # Step 5: remove overlapping times rows.

    df = reset_steps_uno(df)

    # Step 6: trim steps from overlapping times.
    df = trim_steps_from_overlapping_times(df)

    df = reset_steps_uno(df)

    df = df[df['duration'] > 1.0e-5]

    df = reset_steps_dos(df)
    df = reset_steps_uno(df)

    return df


def distance_clean_function(soup):
    '''This function takes all ther other functions and puts it together.'''

    dist_df = clean_distance_data(soup)  # Step 1: create a df from xml data

    dur_df = clean_duration(dist_df)  # Step 2: create a new df to clean values

    dist_df.drop(columns=['start_date', 'end_date'], inplace=True)

    # Step 3: xml input file all parsed
    df = pd.concat([dist_df, dur_df], axis=1)

    df = df[['start_date', 'start_time', 'end_date',
             'end_time', 'tot_dist', 'duration', 'source']]

    df = reset_distance_uno(df)

    '''I found working with numbers easier than working with Timedeltas'''
    df.loc[:, 'start_time'] = pd.to_numeric(df['start_time']) / 3600000000000
    df.loc[:, 'end_time'] = pd.to_numeric(df['end_time']) / 3600000000000
    df.loc[:, 'duration'] = pd.to_numeric(df['duration']) / 3600000000000

    df = split_distance_between_days(df)  # Step 4: split multi-day data.

    df = reset_distance_uno(df)
    df = reset_distance_dos(df)

    df = remove_overlap_time_rows(df)  # Step 5: remove overlapping times rows.

    df = reset_distance_uno(df)
    df = reset_distance_dos(df)

    # Step 6: trim distance from overlapping times.
    df = trim_distance_from_overlapping_times(df)

    df = reset_distance_uno(df)
    df = reset_distance_dos(df)

    df = df[df['duration'] > 1.0e-5]

    df = reset_distance_uno(df)
    df = reset_distance_dos(df)

    return df
