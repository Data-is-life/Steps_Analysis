import pandas as pd


def all_interesting_stats(df, df_w, df_m, df_sd, df_td):
    '''This function checks most and least values for the day, month, week,
    rolling 7 days, and rolling 30 days'''

    m_s_d = df.num_steps.max()  # Check for most steps in a day
    m_s_w = df_w.num_steps.max()  # Check for most steps in a week
    m_s_m = df_m.num_steps.max()  # Check for most steps in a month
    m_s_tf = df_tf.num_steps.max()  # Check for most steps in a 24 hour period
    m_s_sd = df_sd.num_steps.max()  # Check for most steps in a 7 day period
    m_s_td = df_td.num_steps.max()  # Check for most steps in a 30 day period

    l_s_d = df.num_steps.min()  # Check for least steps in a day
    l_s_w = df_w.num_steps.min()  # Check for least steps in a week
    l_s_m = df_m.num_steps.min()  # Check for least steps in a month
    l_s_tf = df_tf.num_steps.min()  # Check for least steps in a 24 hour period
    l_s_sd = df_sd.num_steps.min()  # Check for least steps in a 7 day period
    l_s_td = df_td.num_steps.min()  # Check for least steps in a 30 day period

    # Score = mean/variance
    m_sc_w = df_w.mv_score.max() # Check for highest score in a week.
    m_sc_m = df_m.mv_score.max()  # Check for highest score in a month
    m_sc_sd = df_sd.mv_score.max()  # Check for highest score in a 7 day period
    m_sc_td = df_td.mv_score.max()  # Check for highest score in a 30 day period

    l_sc_w = df_w.mv_score.min()  # Check for lowest score in a week
    l_sc_m = df_m.mv_score.min()  # Check for lowest score in a month
    l_sc_sd = df_sd.mv_score.min()  # Check for highest score in a 7 day period
    l_sc_td = df_td.mv_score.min()  # Check for highest score in a 30 day period

    m_v_w = df_w.varian.max()  # Check for highest variance in a week
    m_v_m = df_m.varian.max()  # Check for highest variance in a month
    m_v_sd = df_sd.varian.max()  # Check for highest variance in a 7 day period
    m_v_td = df_td.varian.max()  # Check for highest variance in a 30 day period

    l_v_w = df_w.varian.min()  # Check for lowest variance in a week
    l_v_m = df_m.varian.min()  # Check for lowest variance in a month
    l_v_sd = df_sd.varian.min()  # Check for lowest variance in a 7 day period
    l_v_td = df_td.varian.min()  # Check for lowest variance in a 30 day period

    high_stp_day = str(df[df['num_steps'] == m_s_d]['start_date'].values)[
        2:12]  # Gets the date
    low_stp_day = str(df[df['num_steps'] == l_s_d]['start_date'].values)[
        2:12]  # Gets the date

    high_stp_week = str(df_w[df_w['num_steps'] == m_s_w][
                        'week_dates'].values)[2:12]  # Gets the week dates
    high_var_week = str(df_w[df_w['num_steps'] == m_v_w][
                        'week_dates'].values)[2:12]  # Gets the week dates
    ma_week = str(df_w[df_w['num_steps'] == m_sc_w]['week_dates'].values)[
        2:12]  # Gets the week dates

    low_stp_week = str(df_w[df_w['num_steps'] == l_s_w]
                       ['week_dates'].values)[2:12]  # Gets the week dates
    low_var_week = str(df_w[df_w['num_steps'] == l_v_w]
                       ['week_dates'].values)[2:12]  # Gets the week dates
    la_week = str(df_w[df_w['num_steps'] == l_sc_w]['week_dates'].values)[
        2:12]  # Gets the week dates

    high_stp_month = str(df_m[df_m['num_steps'] == m_s_m][
                         'month'].values)[2:12]  # Gets the month name & year
    high_var_month = str(df_m[df_m['num_steps'] == m_v_m][
                         'month'].values)[2:12]  # Gets the month name & year
    ma_month = str(df_m[df_m['num_steps'] == l_v_m]['month'].values)[
        2:12]  # Gets the month name & year

    low_stp_month = str(df_w[df_w['num_steps'] == m_sc_m][
                        'week_dates'].values)[2:12]  # Gets the month name & year
    low_var_month = str(df_m[df_m['num_steps'] == l_s_m]['month'].values)[
        2:12]  # Gets the month name & year
    la_month = str(df_m[df_m['num_steps'] == l_sc_m]
                   ['week_dates'].values)[2:12]  # Gets the month name & year

    high_stp_twfr_hour = str(df_tf[df_tf['num_steps'] == m_s_tf][
                             'start_date'].values)[2:12]  # Gets the dates of the 24 hour period
    low_stp_twfr_hour = str(df_tf[df_tf['num_steps'] == l_s_tf][
                            'start_date'].values)[2:12]  # Gets the dates of the 24 hour period

    high_stp_seven_day = str(df_sd[df_sd['num_steps'] == m_s_sd][
                             'week_dates'].values)[2:12]  # Gets the dates of the 7 day period
    high_var_seven_day = str(df_sd[df_sd['num_steps'] == m_v_sd][
                             'week_dates'].values)[2:12]  # Gets the dates of the 7 day period
    ma_seven_day = str(df_sd[df_sd['num_steps'] == m_sc_sd][
                       'week_dates'].values)[2:12]  # Gets the dates of the 7 day period
    low_stp_seven_day = str(df_sd[df_sd['num_steps'] == l_s_sd][
                            'week_dates'].values)[2:12]  # Gets the dates of the 7 day period
    low_var_seven_day = str(df_sd[df_sd['num_steps'] == l_v_sd][
                            'week_dates'].values)[2:12]  # Gets the dates of the 7 day period
    la_seven_day = str(df_sd[df_sd['num_steps'] == l_sc_sd][
                       'week_dates'].values)[2:12]  # Gets the dates of the 7 day period

    high_stp_thirty_day = str(df_td[df_td['num_steps'] == m_s_td][
                              'week_dates'].values)[2:12]  # Gets the dates of the 30 day period
    high_var_thirty_day = str(df_td[df_td['num_steps'] == m_v_td][
                              'week_dates'].values)[2:12]  # Gets the dates of the 30 day period
    ma_thirty_day = str(df_td[df_td['num_steps'] == m_sc_td][
                        'week_dates'].values)[2:12]  # Gets the dates of the 30 day period
    low_stp_thirty_day = str(df_td[df_td['num_steps'] == l_s_td][
                             'week_dates'].values)[2:12]  # Gets the dates of the 30 day period
    low_var_thirty_day = str(df_td[df_td['num_steps'] == l_v_td][
                             'week_dates'].values)[2:12]  # Gets the dates of the 30 day period
    la_thirty_day = str(df_td[df_td['num_steps'] == l_sc_td][
                        'week_dates'].values)[2:12]  # Gets the dates of the 30 day period

    '''This creates a dictionary of all the values, so they are easy to display.'''
    result = {'most_steps_day': [high_stp_day, m_s_d],

              'least_steps_day': [low_stp_day, l_s_d],

              'most_steps_week': [high_stp_week, m_s_w],
              'highest_variance_week': [high_var_week, m_v_w],
              'most_active_week': [ma_week, m_sc_w],

              'least_steps_week': [low_stp_week, l_s_w],
              'lowest_variance_week': [low_var_week, l_v_w],
              'least_active_week': [la_week, l_sc_w],

              'most_steps_month': [high_stp_month, m_s_m],
              'highest_var_month': [high_var_month, m_v_m],
              'most_active_month': [ma_month, m_sc_m],

              'least_steps_month': [low_stp_month, l_s_m],
              'lowest_var_month': [low_var_month, l_v_m],
              'least_active_month': [la_month, l_sc_m],

              'most_steps_tf_hours': [high_stp_twfr_hour, m_s_tf],
              'least_steps_tf_hours': [low_stp_twfr_hour, l_s_tf],

              'most_steps_seven_days': [high_stp_seven_day, m_s_sd],
              'highest_var_seven_days': [high_var_seven_day, m_v_sd],
              'most_active_seven_days': [ma_seven_day, m_sc_sd],

              'least_steps_seven_days': [low_stp_seven_day, l_s_sd],
              'lowest_var_seven_days': [low_var_seven_day, l_v_sd],
              'least_active_seven_days': [la_seven_day, l_sc_sd],

              'most_steps_thirty_days': [high_stp_thirty_day, m_s_td],
              'highest_var_thirty_days': [high_var_thirty_day, m_v_td],
              'most_active_thirty_days': [ma_thirty_day, m_sc_td],

              'least_steps_thirty_days': [low_stp_thirty_day, l_s_td],
              'lowest_var_thirty_days': [low_var_thirty_day, l_v_td],
              'least_active_thirty_days': [la_thirty_day, l_sc_td]
              }

    return result