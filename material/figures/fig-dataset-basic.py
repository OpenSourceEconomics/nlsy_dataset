#!/usr/bin/env python
"""This module creates some auxiliary graphs for the discussion of the dataset."""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

from auxiliary import SURVEY_YEARS
from auxiliary import get_dataset
from auxiliary import get_other_dataset


def set_formatter(ax):
    """This function ensures a pretty formatting"""
    formatter = matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    ax.get_yaxis().set_major_formatter(formatter)


df = get_dataset()
df79 = get_other_dataset()

# We want to plot the number of observations over time.
num_obs = []
for year in SURVEY_YEARS:
    cond = df['IS_INTERVIEWED'].loc[:, year].isin([True])
    num_obs += [df['IDENTIFIER'].loc[:, year][cond].count()]

ax = plt.figure().add_subplot(111)
set_formatter(ax)

ax.bar(df['SURVEY_YEAR'].unique(), num_obs)

ax.set_ylabel('Observations')
ax.set_xlabel('Year')

plt.savefig('fig-dataset-basic-observations.png')

# We want to plot gender.
dat = df['GENDER'].loc[:, 1978].astype('category')
dat = dat.cat.rename_categories({1: 'Male', 2: 'Female'})

ax = plt.figure().add_subplot(111)
ax.pie(dat.value_counts(normalize=True), labels=['Male', 'Female'], autopct='%1.1f%%')

plt.savefig('fig-dataset-basic-gender.png')

'''
# We want to plot ethnic origin.
df['RACE_NEW'] = np.nan
cond = df['SAMPLE_ID'].isin([1, 2, 5, 6, 9, 12, 15, 18])
df.loc[cond, 'RACE_NEW'] = 'White'

cond = df['SAMPLE_ID'].isin([3, 7, 10, 13, 16, 19])
df.loc[cond, 'RACE_NEW'] = 'Black'

cond = df['SAMPLE_ID'].isin([4, 811, 14, 17, 20])
df.loc[cond, 'RACE_NEW'] = 'Hispanic'


ax = plt.figure().add_subplot(111)

dat = df['RACE_NEW'].loc[:, 1978].astype('category')
ax.pie(dat.value_counts(normalize=True), labels=['White', 'Black', 'Hispanic'], autopct='%1.1f%%')
plt.savefig('fig-dataset-basic-race.png')
'''

# We want to plot income quartiles.
first_q = np.percentile(df79['TNFI_TRUNC'], 25)
second_q = np.percentile(df79['TNFI_TRUNC'], 50)
third_q = np.percentile(df79['TNFI_TRUNC'], 75)


q1 = df79.loc[lambda df: df.TNFI_TRUNC < first_q, :]
total_q_1 = q1['TNFI_TRUNC'].sum()

q2 = df79.loc[lambda df: df.TNFI_TRUNC < second_q, :]
total_q_2 = q2['TNFI_TRUNC'].sum() - total_q_1

q3 = df79.loc[lambda df: df.TNFI_TRUNC < third_q, :]
total_q_3 = q3['TNFI_TRUNC'].sum() - total_q_2

total_q_4 = df79['TNFI_TRUNC'].sum() - total_q_3

dat = [total_q_1, total_q_2, total_q_3, total_q_4]
ax = plt.figure().add_subplot(111)
ax.pie(dat, labels=['First quartile', 'Second quartile', 'Third quartile',
                    'Fourth quartile'], autopct='%1.1f%%')

plt.savefig('fig-dataset-basic-income-quartile.png')

# We want to plot the years of birth. For pretty formatting, we remove years of birth with only a
# very small number of individuals.
dat = df['YEAR_OF_BIRTH'].loc[:, 1978]
dat = dat.value_counts().to_dict()

for year in [1955, 1956, 1965]:
    del dat[year]

ax = plt.figure().add_subplot(111)
set_formatter(ax)

ax.set_ylabel('Observations')
ax.set_xlabel('Year of Birth')

ax.bar(dat.keys(), dat.values())

plt.savefig('fig-dataset-basic-birth.png')

# We want to plot the relative shares of the different samples.
df['SAMPLE'] = df['SAMPLE_ID'].loc[:, 1978].copy()
cond = df['SAMPLE_ID'].isin(range(9))
df.loc[cond, 'SAMPLE'] = 'Cross-sectional sample'

cond = df['SAMPLE_ID'].isin(range(9, 15))
df.loc[cond, 'SAMPLE'] = 'Supplementary sample'

cond = df['SAMPLE_ID'].isin(range(15, 21))
df.loc[cond, 'SAMPLE'] = 'Military sample'

ax = plt.figure().add_subplot(111)

dat = df['SAMPLE'].loc[:, 1978].astype('category')

labels = ['Cross-sectional', 'Supplementary', 'Military']
ax.pie(dat.value_counts(normalize=True), labels=labels, autopct='%1.1f%%')
plt.savefig('fig-dataset-basic-samples.png')
