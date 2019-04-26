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
Copyright (c) 2019, Mohit Gangwani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Stay tuned, there is more to come!**
