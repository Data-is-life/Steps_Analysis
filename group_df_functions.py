# Author: Mohit Gangwani
# Date: 11/02/2018
# Git-Hub: Data-is-Life

import pandas as pd
import numpy as np



def create_month_df(df):
	pass
def create_weekley_df(df):
	pass
def create_seven_day_rolling_df(df):
	pass
def create_thirty_day_rolling_df(df):
	pass






def sum_day_df(df):
    summed_df = df.groupby(by=['start_date']).sum()
    summed_df.reset_index(inplace=True)
    summed_df['steps_per_hour'] = summed_df[
        'num_steps'] / summed_df['duration']
    summed_df.drop(columns=['start_time', 'end_time'], inplace=True)
    return summed_df


def mean_day_df(df):
    mean_df = df.groupby(by=['start_date']).mean()
    mean_df.reset_index(inplace=True)
    mean_df['steps_per_hour'] = mean_df[
        'num_steps'] / mean_df['duration']
    return mean_df


def median_day_df(df):
    median_df = df.groupby(by=['start_date']).median()
    median_df.reset_index(inplace=True)
    median_df['steps_per_hour'] = median_df[
        'num_steps'] / median_df['duration']
    return median_df


def sum_month_df(df):
	summed_df = df.groupby(by=['start_date']).sum()
    summed_df.reset_index(inplace=True)
    summed_df['steps_per_hour'] = summed_df[
        'num_steps'] / summed_df['duration']
    summed_df.drop(columns=['start_time', 'end_time'],inplace=True)
    return summed_df


def mean_month_df(df):
	mean_df = df.groupby(by=['start_date']).mean()
    mean_df.reset_index(inplace=True)
    mean_df['steps_per_hour'] = mean_df[
        'num_steps'] / mean_df['duration']
    return mean_df


def median_month_df(df):
	median_df = df.groupby(by=['start_date']).median()
    median_df.reset_index(inplace=True)
    median_df['steps_per_hour'] = median_df[
        'num_steps'] / median_df['duration']
    return median_df


def sum_week_df(df):
	summed_df = df.groupby(by=['start_date']).sum()
    summed_df.reset_index(inplace=True)
    summed_df['steps_per_hour'] = summed_df[
        'num_steps'] / summed_df['duration']
    summed_df.drop(columns=['start_time', 'end_time'])
    return summed_df


def mean_week_df(df):
	mean_df = df.groupby(by=['start_date']).mean()
    mean_df.reset_index(inplace=True)
    mean_df['steps_per_hour'] = mean_df[
        'num_steps'] / mean_df['duration']
    mean_df.drop(columns=['start_time', 'end_time'], inplace=True)
    return mean_df


def median_week_df(df):
	median_df = df.groupby(by=['start_date']).median()
    median_df.reset_index(inplace=True)
    median_df['steps_per_hour'] = median_df[
        'num_steps'] / median_df['duration']
    return median_df
