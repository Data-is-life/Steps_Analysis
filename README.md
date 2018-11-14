# Project Fix iHealth Data

<p> Creating an app for cleaning redundant data on iHealth from a smart watch and iPhone.<br>
<br>
Working on the following measurements:

- Number of steps
- Distance
- Elevation

## Data:
All the data (currently) is from my iPhone.

## Analysis & Vizualizations:

Following ways to analyze and vizualize the amount of __steps taken__ + __distance walked/ran__ + __"flights climbed"__. 

(I put the __flights climbed__ in a quotation, since iPhone considers the uphill elevation as __flights climbed__):

1. Daily - Graphs (iPhone already does that fairly well. I will be still doing it since there is no way to customize the time period to view)
2. Weekly - Graphs (Same explanation as above)
3. Monthly - Graphs (Same explanation as above)
4. Scoring
    - Weekly
    - Monthly
    - 7 Day rolling
    - 30 Day rolling
    - Custom time period rolling
    - All the days of the week for the year (eg: All Mondays, Tuesdays, etc.)
    - All the days of the month for the year (eg: the 1st of the month, the 2nd, etc.)

### Scoring:
Some might think that the most amount of steps taken, distance walked/ran, or flights climbed would be the best week, month, or any other metric. 

This is where I would disagree. For example:

In a week where one walked/ran 15 miles or 30,000 steps on one day and walked less than a mile or less than 2,500 steps for the rest of the week. I would not call that the best week, since one day of extreme activity would not reflect that week to be the most active.

So, I will be using a different metric to judge that. To start off, I will be using the Inverse Coefficient of Variation (ICV - mean devided by the standard deviation) to give the time periods a score.

Some might argue using Index of Dispersion (ID - variance over mean) would make more sense. I have looked at it and the ID gives a high score to even the time periods where the total may not be as high.

## Usage
Clone this repository with the command

```
git clone git@github.com:Data-is-life/Steps_Analysis.git
```

All codes are located in **src** folder.

## Repository Structure
The repository has the following structure.

```
├── data
│   └── export.xml
├── docs
├── README.md
└── src
    ├── all_distance_functions.py
    ├── all_steps_functions.py
    ├── common_cleaning_functions.py
    ├── distance_analysis.ipynb
    ├── distance_analysis.py
    ├── group_df_functions.py
    ├── main_clean_functions.py
    ├── __stats_functions.py
    ├── stats_functions.py
    ├── testing_dist_and_steps_funcs.ipynb
    └── unused_functions.py
```
## Tools used so far:

- Pandas
- Numpy
- Beautiful Soup

<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="300"></br>
<img src="https://pandas.pydata.org/_static/pandas_logo.png" width="300"></br>
<img src="https://bids.berkeley.edu/sites/default/files/styles/400x225/public/projects/numpy_project_page.jpg?itok=flrdydei" width="300"></br>
<img src="https://tettra.co/culture-codes/wp-content/logos/github.png" width="300"></br>
<img src="https://funthon.files.wordpress.com/2017/05/bs.png?w=1200" width="300">


```
Copyright (c) 2018, Mohit Gangwani

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

**Stay tuned, there is more to come!**
