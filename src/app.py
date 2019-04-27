# Author: Mohit Gangwani
# Date: 04/25/2019
# Git-Hub: Data-is-Life


from bs4 import BeautifulSoup
import gc
from numpy import where
from pandas import to_timedelta as ToTd
from pandas import to_datetime as ToDt
from pandas import to_numeric as ToNm
from pandas import DataFrame as DF
from pandas import concat
gc.enable()


class CleanerHelper(object):

    def __init__(self):
        pass

    def reset_drop(self, df):
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        return df

    def sort_drop(self, df):
        df.sort_values(by=['start_date', 'end_date'], inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        return df


class TrimData(object):

    def __init__(self, soup_obj, speed_unit, measure_unit):
        super(TrimData, self).__init__()
        self.soup_obj = soup_obj
        self.speed_unit = speed_unit
        self.measure_unit = measure_unit
        self.one_day = ToTd(1, 'D')
        self.two_days = ToTd(2, 'D')
        self.twh = 24 - 1e-6
        self.ch = CleanerHelper()

    def parse_soup(self):
        self.df = DF()
        '''Insert the values in the original dataframe. Convert time to
           numerical format to make calculations easier.'''
        self.df.loc[:, 'start_date'] = [d['startDate'] for d in self.soup_obj]
        self.df.loc[:, 'end_date'] = [d['endDate'] for d in self.soup_obj]
        self.df.loc[:, self.measure_unit] = [d['value'] for d in self.soup_obj]
        self.df.loc[:, 'source'] = [d['sourceName'] for d in self.soup_obj]
        self.df.loc[
            :, self.measure_unit] = self.df[self.measure_unit].astype(float)
        return self.df

    def clean_set(self):
        '''Split start and end date, time, and timezone to a new df. Drop the
           Timezone column.'''
        start_date_df = self.df.start_date.str.split(
            ' ', expand=True).drop(columns=[2])
        end_date_df = self.df.end_date.str.split(
            ' ', expand=True).drop(columns=[2])

        # Merge the start and end date & time to a single value.
        start_date_df.loc[:, 'std'] = start_date_df[0] + ' ' + start_date_df[1]
        end_date_df.loc[:, 'etd'] = end_date_df[0] + ' ' + end_date_df[1]

        # Convert the date to `datetime` and time to `timedelta`
        start_date_df.loc[:, 'sd'] = ToDt(start_date_df[0], format='%Y-%m-%d')
        end_date_df.loc[:, 'ed'] = ToDt(end_date_df[0], format='%Y-%m-%d')

        start_date_df.loc[:, 'st'] = ToTd(start_date_df[1])
        end_date_df.loc[:, 'et'] = ToTd(end_date_df[1])

        '''Insert the values in the original dataframe. Convert time to
           numerical format to make calculations easier.'''
        self.df.loc[:, 'start_date'] = start_date_df.sd.copy()
        self.df.loc[:, 'start_time'] = ToNm(start_date_df.st) / 3.6e12
        self.df.loc[:, 'end_date'] = end_date_df.ed.copy()
        self.df.loc[:, 'end_time'] = ToNm(end_date_df.et) / 3.6e12
        self.df.loc[:, 'duration'] = ToNm(
            (end_date_df.ed + end_date_df.et) - (
                start_date_df.sd + start_date_df.st)) / 3.6e12

        gc.collect()
        return self.df

    def trim_one(self):
        self.df.loc[:, self.speed_unit] = self.df[
            self.measure_unit] / self.df['duration']
        # Create two different dfs to do separate calculations.
        ndf1 = self.df[
            self.df.start_date + self.one_day == self.df.end_date].copy()
        ndf2 = ndf1.copy()

        '''Calculations for the first data frame are to trim values till the
           end of the first day. The calculations are done as follow:
           1. End date is the start date
           2. End time is 23.9999999999999999999
           3. Duration is from starting time till midnight
           4. the `measure_unit` is calculated by multiplying the `speed_unit`
           and the new calculated duration.
           5. Reset the index'''
        ndf1.loc[:, 'end_date'] = ndf1['start_date'].copy()
        ndf1.loc[:, 'end_time'] = self.twh
        ndf1.loc[:, 'duration'] = ndf1['end_time'] - ndf1['start_time']
        ndf1.loc[:, self.measure_unit] = ndf1[self.speed_unit] * ndf1.duration
        ndf1 = self.ch.reset_drop(ndf1)

        '''Calculations for the second df are to trim values starting at
           midnight of the following day. The calculations are done as follow:
           1. Start date is the end date
           2. Start time is 0.0
           3. Duration is from midnight till the ending time  
           4. the `measure_unit` is calculated by multiplying the `speed_unit`
              and the new calculated duration.
           5. Reset the index'''
        ndf2.loc[:, 'start_date'] = ndf2['end_date'].copy()
        ndf2.loc[:, 'start_time'] = 0.0
        ndf2.loc[:, 'duration'] = ndf2['end_time'] - ndf2['start_time']
        ndf2.loc[:, self.measure_unit] = ndf2[self.speed_unit] * ndf2.duration
        ndf2 = self.ch.reset_drop(ndf2)

        '''Drop the rows where the data spills to the next day, and append the
           new calculated values'''
        self.df = self.df[
            self.df.start_date + self.one_day != self.df.end_date].copy()
        self.df = self.df.append(
            [ndf1, ndf2], ignore_index=True, sort=False)
        self.df.sort_values(
            by=['start_date', 'start_time', 'end_time'], inplace=True)
        self.df = self.ch.reset_drop(self.df)
        return self.df

    def trim_two(self):
        self.df.loc[
            :, self.speed_unit] = self.df[self.measure_unit] / self.df.duration
        # Create three different dfs to do separate calculations.
        ndf1 = self.df[
            self.df.start_date + self.two_days == self.df.end_date].copy()
        ndf2 = ndf1.copy()
        ndf3 = ndf1.copy()

        '''Calculations for the first data frame are to trim values till the
           end of the first day. The calculations are done as follow:
           1. End date is the start date
           2. End time is 23.9999999999999999999
           3. Duration is from starting time till midnight
           4. the `measure_unit` is calculated by multiplying the `speed_unit`
              and the new calculated duration.
           5. Reset the index'''
        ndf1.loc[:, 'end_date'] = ndf1['start_date'].copy()
        ndf1.loc[:, 'end_time'] = self.twh
        ndf1.loc[:, 'duration'] = self.twh - ndf1['start_time']
        ndf1.loc[:, self.measure_unit] = ndf1[self.speed_unit] * ndf1.duration
        ndf1 = self.ch.reset_drop(ndf1)

        '''Calculations for the second data frame are to trim values till the
           end of the first day. The calculations are done as follow:
           1. End date and start date are one day after the starting date
           2. Start time is 0.0
           3. End time is 23.9999999999999999999
           4. Duration is 24 hours
           5. the `measure_unit` is calculated by multiplying the `speed_unit`
              and the new calculated duration = 24 hours.
           6. Reset the index'''
        ndf2.loc[:, 'start_date'] = ndf2['start_date'] + self.one_day
        ndf2.loc[:, 'end_date'] = ndf2['start_date'] + self.one_day
        ndf2.loc[:, 'start_time'] = 0
        ndf1.loc[:, 'end_time'] = self.twh
        ndf2.loc[:, 'duration'] = self.twh
        ndf2.loc[:, self.measure_unit] = ndf2[self.speed_unit] * self.twh
        ndf2 = self.ch.reset_drop(ndf2)

        '''Calculations for the third df are to trim values starting at
           midnight of the last day. The calculations are done as follow:
           1. Start date is the end date
           2. Start time is 0.0
           3. Duration is from midnight till the ending time  
           4. the `measure_unit` is calculated by multiplying the `speed_unit`
              and the new calculated duration.
           5. Reset the index'''
        ndf3.loc[:, 'start_date'] = ndf3['end_date'].copy()
        ndf3.loc[:, 'start_time'] = 0
        ndf3.loc[:, 'duration'] = ndf3['end_time'].copy()
        ndf3.loc[:, self.measure_unit] = ndf3[self.speed_unit] * ndf3.duration
        ndf3 = self.ch.reset_drop(ndf3)

        '''Drop the rows where the data spills to two days, and append the
           new calculated values'''
        self.df = self.df[
            self.df.start_date + self.two_days != self.df.end_date].copy()
        self.df = self.df.append(
            [ndf1, ndf2, ndf3], ignore_index=True, sort=False)
        self.df.sort_values(
            by=['start_date', 'start_time', 'end_time'], inplace=True)
        self.df = self.ch.reset_drop(self.df)

        return self.df

    def overlapping_rows(self):
        '''Creating three conditions:
           1. The start time of the row has to be greater than the start time
              of the next row.
           2. The end time of the row has to be less than the end time of the
              next row.
           3. The start date of the row has to be same than the start date of
              the next row.
           If all conditions match, the row is dropped, since we already had
           data for that time.'''
        ldf = len(self.df)
        pdf = 0
        while ldf != pdf:
            ldf = len(self.df)
            self.df.loc[:, 'cond1'] = where(
                self.df.start_time >= self.df.start_time.shift(1), 1, 0)
            self.df.loc[:, 'cond2'] = where(
                self.df.end_time <= self.df.end_time.shift(1), 1, 0)
            self.df.loc[:, 'cond3'] = where(
                self.df.start_date == self.df.start_date.shift(1), 1, 0)
            self.df.loc[:, 'condsum'] = (
                self.df.cond1 + self.df.cond2 + self.df.cond3)
            self.df = self.df[self.df['condsum'] < 3].copy()
            pdf = len(self.df)

        gc.collect()
        self.df.reset_index(inplace=True)
        self.df.drop(columns=['cond1', 'cond2', 'cond3',
                              'condsum', 'index'], inplace=True)
        return self.df

    def trim_dur(self):
        '''Creating three conditions:
           1. The end time of the row has to be greater than the start time of
              the next row.
           2. The start date of the row has to be same than the start date of
              the next row.
           3. The sources have to be different, otherwise, we are just
              grouping all the data.'''
        self.df.loc[:, 'cond1'] = where(
            self.df.end_time >= self.df.start_time.shift(1), 1, 0)
        self.df.loc[:, 'cond2'] = where(
            self.df.start_date == self.df.start_date.shift(1), 1, 0)
        self.df.loc[:, 'conds'] = where(
            self.df.source != self.df.source.shift(1), 1, 0)
        self.df.loc[:, 'condsum'] = (
            self.df.cond1 + self.df.cond2 + self.df.conds)
        self.df.drop(columns=['cond1', 'cond2', 'conds'], inplace=True)

        # Duration is recalculated to make sure it is right.
        self.df.loc[:, 'duration'] = self.df.end_time - self.df.start_time

        '''Data is trimmed from a row if all the conditions match.
           Following calculations are performed if all the conditions match:
           1. The start time of the row is the end time of the previous row.
           2. Duration is recalculated.
           3. `measure_unit` is recalculated by multiplying the new duration
              and the `speed_unit`.'''
        self.df.loc[:, 'start_time'] = where(
            self.df.condsum == 3, self.df.end_time.shift(1) - 1e-6,
            self.df.start_time)
        self.df.loc[:, 'duration'] = where(
            self.df.condsum == 3, self.df.end_time - self.df.start_time,
            self.df.duration)
        self.df.loc[:, self.measure_unit] = where(
            self.df.condsum == 3, self.df.duration * self.df[self.speed_unit],
            self.df[self.measure_unit])

        self.df.reset_index(inplace=True)
        self.df.drop(columns=['index', 'condsum'], inplace=True)
        return self.df

    def run_all(self):
        self.df = self.parse_soup()
        self.df = self.ch.sort_drop(self.df)
        self.df = self.clean_set()
        self.df = self.trim_one()
        self.df = self.trim_two()
        self.df = self.overlapping_rows()
        self.df = self.trim_dur()
        self.df = self.ch.sort_drop(self.df)
        self.df = self.trim_one()
        self.df = self.trim_two()
        self.df = self.overlapping_rows()
        self.df = self.trim_dur()
        self.df.drop(columns=['start_time', 'end_time',
                              'duration'], inplace=True)
        daily_df = self.df.groupby(by=['start_date', 'end_date']).sum()
        return self.df, daily_df


class FXYRS(object):

    def __init__(self, file_name):
        super(FXYRS, self).__init__()
        self.file_name = file_name

    def clean(self):
        ch = CleanerHelper()
        # Step 1: Get data from xml using BeautifulSoup
        with open(self.file_name) as fp:
            soup = BeautifulSoup(fp, 'lxml-xml')

        '''Step 2: Parse all the flights climbed, distance walked, and steps
        taken data to a dictionary like format that makes it easy to extract
        values.'''
        fp_ = 'HKQuantityTypeIdentifier'
        flights = soup.findAll('Record', {'type': f'{fp_}FlightsClimbed'})
        distance = soup.findAll(
            'Record', {'type': f'{fp_}DistanceWalkingRunning'})
        steps = soup.findAll('Record', {'type': f'{fp_}StepCount'})

        '''Step 3: Create distance, steps, and flights dfs from the xml data
        using the TrimData class.'''
        floors_set = TrimData(flights, 'fph', 'num_floors')
        fdf, ffdf = floors_set.run_all()

        dist_set = TrimData(distance, 'mph', 'tot_dist')
        ddf, dddf = dist_set.run_all()

        steps_set = TrimData(steps, 'sph', 'num_steps')
        sdf, dsdf = steps_set.run_all()

        cdf = concat([dsdf, dddf, ffdf], sort=False, axis=1)

        cdf.loc[:, 'ft_per_step'] = cdf.tot_dist * 5280 / cdf.num_steps
        cdf.drop(columns=['sph', 'mph', 'fph'], inplace=True)

        cdf.reset_index(inplace=True)
        cdf.fillna(0, inplace=True)

        return fdf, ddf, sdf, cdf
