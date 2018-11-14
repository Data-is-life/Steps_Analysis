# Author: Mohit Gangwani
# Date: 11/13/2018
# Git-Hub: Data-is-Life

import pandas as pd


def drop_change_rename_df(df, x, col_rnm):

    df.drop(df.index[list(range(x - 1))], inplace=True)
    df.reset_index(inplace=True)
#     df.drop(columns=['index'], inplace=True)
    df.loc[:, 'start_date'] = df['end_date'] - pd.Timedelta(x, unit='D')
    df.rename(columns={'num_steps': col_rnm + 'num_steps'}, inplace=True)
    if 'index' in df.columns:
        df.drop(columns=['index'], inplace=True)
    df.set_index(['start_date', 'end_date'], inplace=True)

    return df


def rolling_day_df(df, x):
    df.set_index(['start_date', 'end_date'], inplace=True)

    m_df = df.rolling(x).mean()
    m_df.reset_index(inplace=True)

    md_df = df.rolling(x).median()
    md_df.reset_index(inplace=True)

    std_df = df.rolling(x).std()
    std_df.reset_index(inplace=True)

    s_df = df.rolling(x).sum()
    s_df.reset_index(inplace=True)

    min_df = df.rolling(x).min()
    min_df.reset_index(inplace=True)

    max_df = df.rolling(x).max()
    max_df.reset_index(inplace=True)

    m_df = drop_change_rename_df(m_df, x, 'mean_')
    md_df = drop_change_rename_df(md_df, x, 'median_')
    merged_df_uno = pd.merge(m_df, md_df, on=m_df.index)

    std_df = drop_change_rename_df(std_df, x, 'std_')
    s_df = drop_change_rename_df(s_df, x, 'total_')
    merged_df_dos = pd.merge(std_df, s_df, on=std_df.index)

    min_df = drop_change_rename_df(min_df, x, 'min_')
    max_df = drop_change_rename_df(max_df, x, 'max_')
    merged_df_tres = pd.merge(min_df, max_df, on=min_df.index)

    merged_df_quatro = pd.merge(merged_df_uno, merged_df_dos,
                                on=merged_df_uno.index)

    merged_df_finale = pd.merge(merged_df_quatro, merged_df_tres,
                                on=merged_df_tres.index)

    merged_df_finale.drop(columns=['key_0_y'], inplace=True)

    merged_df_finale['steps_score_mean'] = merged_df_finale['mean_num_steps'] / \
        merged_df_finale['std_num_steps']

    merged_df_finale['steps_score_median'] = merged_df_finale['median_num_steps'] / \
        merged_df_finale['std_num_steps']

    merged_df_finale.reset_index(inplace=True)

    merged_df_finale.drop(columns=['index', 'key_0'], inplace=True)

    return merged_df_finale
