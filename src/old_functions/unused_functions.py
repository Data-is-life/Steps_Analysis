# i = 0

# while i < len(df)-1:
#     if (df.start_date[i] == df.end_date[i]) and (
#             df.start_date[i] == df.end_date[i+1]) and(
#             df.start_date[i] == df.start_date[i+1]) and (
#             (df.end_time[i] - df.start_time[i+1]) <= 1.0e-5):

#         df.loc[i, 'end_time'] = df.end_time[i+1]
#         df.loc[i, 'num_steps'] = df.num_steps[i] + df.num_steps[i+1]

#         df.drop(index=(i+1), inplace=True)
#         df.reset_index(inplace=True)
#         df.drop(columns=['index'], inplace=True)

#     else:
#         i += 1
# ------------------------------------------------------------------------------------ #
# i = 0
# while i < len(df)-1:
#     if (df.end_date[i] - pd.Timedelta(86400000000000) == df.start_date[i]) and (
#             df.duration[i] <= 1.0):

#         st_dt, st_tm, end_dt, end_tm, num_st, dur, sauce = df.iloc[i]

#         steps_per_hour = num_st / (end_tm + (24.0 - st_tm))

#         dur_1 = round(steps_per_hour * (24.0 - st_tm))
#         dur_2 = round(steps_per_hour * end_tm)

#         df.loc[i+.1] = [end_dt, 0.0, end_dt, end_tm,
#                         dur_1, end_tm, sauce]

#         df.loc[i] = [st_dt, st_tm, st_dt, 24.0,
#                      dur_2, (24.0 - st_tm), sauce]

#         df.reset_index(inplace=True)
#         df.drop(columns=['index'], inplace=True)

#         i += 1
#     else:
#         i += 1
