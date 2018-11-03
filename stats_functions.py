
def all_interesting_stats(df, df_w, df_m, df_sd, df_td, df_sxd, df_ntd):

    m_s_d = df.num_steps.max()
    m_s_w = df_w.num_steps.max()
    m_s_m = df_m.num_steps.max()
    m_s_tf = df_tf.num_steps.max()
    m_s_sd = df_sd.num_steps.max()
    m_s_td = df_td.num_steps.max()

    l_s_d = df.num_steps.min()
    l_s_w = df_w.num_steps.min()
    l_s_m = df_m.num_steps.min()
    l_s_tf = df_tf.num_steps.min()
    l_s_sd = df_sd.num_steps.min()
    l_s_td = df_td.num_steps.min()

    m_sc_w = df_w.mv_score.max()
    m_sc_m = df_m.mv_score.max()
    m_sc_sd = df_sd.mv_score.max()
    m_sc_td = df_td.mv_score.max()

    l_sc_w = df_w.mv_score.min()
    l_sc_m = df_m.mv_score.min()
    l_sc_sd = df_sd.mv_score.min()
    l_sc_td = df_td.mv_score.min()

    high_stp_day = str(df[df['num_steps'] == m_s_d]['start_date'].values)[2:12]
    low_stp_day = str(df[df['num_steps'] == l_s_d]['start_date'].values)[2:12]

    high_stp_week = str(df_w[df_w['num_steps'] == m_s_w][
                        'week_dates'].values)[2:12]
    high_var_week = str(df_w[df_w['num_steps'] == m_v_w][
                        'week_dates'].values)[2:12]
    ma_week = str(df_w[df_w['num_steps'] == m_sc_w]['week_dates'].values)[2:12]
    low_stp_week = str(df_w[df_w['num_steps'] == l_s_w]
                       ['week_dates'].values)[2:12]
    low_var_week = str(df_w[df_w['num_steps'] == l_v_w]
                       ['week_dates'].values)[2:12]
    la_week = str(df_w[df_w['num_steps'] == l_sc_w]['week_dates'].values)[2:12]

    high_stp_month = str(df_m[df_m['num_steps'] == m_s_m][
                         'month'].values)[2:12]
    high_var_month = str(df_m[df_m['num_steps'] == m_v_m][
                         'month'].values)[2:12]
    low_stp_month = str(df_w[df_w['num_steps'] == m_sc_m][
                        'week_dates'].values)[2:12]
    low_var_month = str(df_m[df_m['num_steps'] == l_s_m]['month'].values)[2:12]
    ma_month = str(df_m[df_m['num_steps'] == l_v_m]['month'].values)[2:12]
    la_month = str(df_m[df_m['num_steps'] == l_sc_m]
                   ['week_dates'].values)[2:12]

    high_stp_twfr_hour = str(df_tf[df_tf['num_steps'] == m_s_tf][
                             'start_date'].values)[2:12]
    low_stp_twfr_hour = str(df_tf[df_tf['num_steps'] == l_s_tf][
                            'start_date'].values)[2:12]

    high_stp_seven_day = str(df_sd[df_sd['num_steps'] == m_s_sd][
                             'week_dates'].values)[2:12]
    high_var_seven_day = str(df_sd[df_sd['num_steps'] == m_v_sd][
                             'week_dates'].values)[2:12]
    ma_seven_day = str(df_sd[df_sd['num_steps'] == m_sc_sd][
                       'week_dates'].values)[2:12]
    low_stp_seven_day = str(df_sd[df_sd['num_steps'] == l_s_sd][
                            'week_dates'].values)[2:12]
    low_var_seven_day = str(df_sd[df_sd['num_steps'] == l_v_sd][
                            'week_dates'].values)[2:12]
    la_seven_day = str(df_sd[df_sd['num_steps'] == l_sc_sd][
                       'week_dates'].values)[2:12]

    high_stp_thirty_day = str(df_td[df_td['num_steps'] == m_s_td][
                              'week_dates'].values)[2:12]
    high_var_thirty_day = str(df_td[df_td['num_steps'] == m_v_td][
                              'week_dates'].values)[2:12]
    ma_thirty_day = str(df_td[df_td['num_steps'] == m_sc_td][
                        'week_dates'].values)[2:12]
    low_stp_thirty_day = str(df_td[df_td['num_steps'] == l_s_td][
                             'week_dates'].values)[2:12]
    low_var_thirty_day = str(df_td[df_td['num_steps'] == l_v_td][
                             'week_dates'].values)[2:12]
    la_thirty_day = str(df_td[df_td['num_steps'] == l_sc_td][
                        'week_dates'].values)[2:12]

    result = {'most_steps_in_a_day': high_stp_day,
              'least_steps_in_a_day': low_stp_day,
              'most_steps_in_a_week': high_stp_week,
              'highest_variance_in_a_week': high_var_week,
              '': ma_week,
              'least_steps_in_a_week': low_stp_week,
              'lowest_variance_in_a_week': low_var_week,
              '': la_week, 
              'most_steps_in_a_month': high_stp_month,
              'highest_variance_in_a_month': high_var_month,
              'least_steps_in_a_month': low_stp_month,
              'lowest_variance_in_a_month': low_var_month,
              '': ma_month,
              '': la_month,
              'most_steps_in_tf_hours': high_stp_twfr_hour,
              'least_steps_in_tf_hours': low_stp_twfr_hour,
              'most_steps_in_seven_days': high_stp_seven_day,
              'highest_variance_in_seven_days': high_var_seven_day,
              '': ma_seven_day,
              'least_steps_in_seven_days': low_stp_seven_day,
              'lowest_variance_in_seven_days': low_var_seven_day,
              '': la_seven_day,
              'most_steps_in_thirty_days': high_stp_thirty_day,
              'highest_variance_in_thirty_days': high_var_thirty_day,
              '': ma_thirty_day,
              'least_steps_in_thirty_days': low_stp_thirty_day,
              'lowest_variance_in_thirty_days': low_var_thirty_day,
              '': la_thirty_day
              }
