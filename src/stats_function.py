

def create_daily_steps_df(df):
    '''To run stats, first thing to do is get total for each day.
       So, group it by start and end date, they should be the same
       get rid of start_time, end_time, and duration columns.'''

    daily_df = df.groupby(by=['start_date', 'end_date']).sum()
    daily_df.drop(columns=['start_time', 'end_time', 'duration'], inplace=True)
    daily_df.reset_index(inplace=True)
    return daily_df