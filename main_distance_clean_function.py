# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd
from all_distance_functions import *


def main_clean_function(file_name):
    '''
    This function takes all ther other functions and puts it together
    '''

    dist_df = cleaning_data(file_name)  # Step 1, get the xml and create a df

    dur_df = clean_duration(dist_df)  # Step 2, create a new df to clean values

    dist_df.drop(columns=['start_date', 'end_date'], inplace=True)

    df = pd.concat([dist_df, dur_df], axis=1)  # Step 3, xml input file all parsed

    df = df[['start_date', 'start_time', 'end_date',
             'end_time', 'tot_dist', 'duration', 'source']]

    df = reset_df_uno(df)

    '''I found working with numbers easier than working with Timedeltas'''
    df.loc[:, 'start_time'] = pd.to_numeric(df['start_time']) / 3600000000000
    df.loc[:, 'end_time'] = pd.to_numeric(df['end_time']) / 3600000000000
    df.loc[:, 'duration'] = pd.to_numeric(df['duration']) / 3600000000000

    df = trim_distance_from_overlapping_times(df)  # Step 4, split multi-day data.

    df = reset_df_uno(df)

    df = remove_overlap_time_rows(df)  # Step 5, remove overlapping times rows.

    df = reset_df_uno(df)


    df = trim_distance_from_overlapping_times(df)  # Step 6, trim distance from overlapping times.

    df = reset_df_uno(df)

    df = df[df['duration'] > 1.0e-5]

    df = reset_df_dos(df)

    df = reset_df_uno(df)

    return df
