# Author: Mohit Gangwani
# Date: 11/14/2018
# Git-Hub: Data-is-Life

import pandas as pd


def clean_flights_data(soup):
    '''Step 1:
       Using Pandas to get a dataframe of all the values.'''

    flights_df = pd.DataFrame()
    start_date_col = []
    end_date_col = []
    num_floors_col = []
    source_col = []

    flights = soup.findAll('Record',
                           {'type': 'HKQuantityTypeIdentifierFlightsClimbed'})

    for num in flights:
        start_date_col.append(num['startDate'])
        end_date_col.append(num['endDate'])
        num_floors_col.append(num['value'])
        source_col.append(num['sourceName'])

    flights_df.loc[:, 'start_date'] = start_date_col
    flights_df.loc[:, 'end_date'] = end_date_col
    flights_df.loc[:, 'num_floors'] = num_floors_col
    flights_df.loc[:, 'source'] = source_col

    flights_df.loc[:, 'num_floors'] = flights_df.num_floors.astype(int)

    flights_df.sort_values(by=['start_date', 'end_date'], inplace=True)
    flights_df = flights_df[flights_df['num_floors'] > 0]
    flights_df.reset_index(inplace=True)
    flights_df.drop(columns=['index'], inplace=True)

    return flights_df


def split_num_flights_between_days(df):
    '''Step : 4
       Split number of flights climbed between days, in case a measurement
       starts on one day and finishes the following or more days from that
       time.'''

    for i in range(len(df) - 1):
        if (df.end_date[i] - pd.Timedelta(1, unit='D') == df.start_date[i]):

            st_dt, st_tm, end_dt, end_tm, num_st, dur, sauce = df.iloc[i]

            flights_per_hour = num_st / (end_tm + (24.0 - st_tm))

            num_st_1 = round(flights_per_hour * (24.0 - st_tm))
            num_st_2 = round(flights_per_hour * end_tm)

            df.loc[i + .1] = [end_dt, 0.0, end_dt, end_tm,
                              num_st_2, end_tm, sauce]

            df.loc[i] = [st_dt, st_tm, st_dt, 24.0,
                         num_st_1, (24.0 - st_tm), sauce]

            df.reset_index(inplace=True)
            df.drop(columns=['index'], inplace=True)

        elif (df.end_date[i] - pd.Timedelta(2, unit='D') == df.start_date[i]):

            st_dt, st_tm, end_dt, end_tm, num_st, dur, sauce = df.iloc[i]
            flights_per_hour = num_st / (end_tm + 24.0 + (24.0 - st_tm))

            num_st_1 = round(flights_per_hour * (24.0 - st_tm))
            num_st_2 = round(flights_per_hour * 24.0)
            num_st_3 = round(flights_per_hour * end_tm)

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


def trim_flights_climbed_from_overlapping_times(df):
    '''Step : 6
       Correct total number of floors climbed and times from overlapping times.

       To trim number of floors climbed, make sure to check if start date for
       the same row are the same and make sure the following row has the same
       starting and ending date.

       Also, the starting time of the following row has to be less than ending
       time for the row to check and the ending time for the following row has
       to be greater.

       Once the number of floors climbed are trimmed, if the remaining floors
       climbed are less than 0.01, drop the row.'''

    for i in range(len(df) - 1):
        if (df.start_date[i] == df.end_date[i]) and (
                df.start_date[i] == df.end_date[i + 1]) and (
                df.start_date[i] == df.start_date[i + 1]) and (
                df.start_time[i + 1] <= df.end_time[i]) and (
                df.end_time[i + 1] >= df.end_time[i]):

            flights_per_hour = df.num_floors[
                i + 1] / (df.end_time[i + 1] - df.start_time[i + 1])

            floors_adjust = (df.end_time[i] - df.start_time[i + 1]
                             ) * flights_per_hour

            floors_adjust = round(floors_adjust)

            df.loc[(i + 1), 'num_floors'] = df.num_floors[i + 1] - \
                floors_adjust
            df.loc[(i + 1), 'start_time'] = df.end_time[i]
            df.loc[(i + 1), 'duration'] = df.end_time[i + 1] - \
                df.start_time[i + 1]

            df.loc[i, 'duration'] = df.end_time[i] - df.start_time[i]
    return df
