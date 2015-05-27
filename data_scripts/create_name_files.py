import pandas as pd
import os
from settings import downloaded_and_valid_fnames
from settings import extract_year_from_fname
from settings import NAMES_FILES_DIR


# init empty dataframe
df = pd.DataFrame(columns = ['name', 'sex', 'count', 'year'])
df.year = df.year.astype(int)
df['count'] = df['count'].astype(int)
topnames = {'M': set(), 'F': set()}
yearcounts = pd.DataFrame(columns=['sex', 'year', 'total', 'top50'])
print("Loading dataframe of all names...")
for fname in downloaded_and_valid_fnames():
    year = extract_year_from_fname(fname)
    xf = pd.read_csv(fname, names = ['name', 'sex', 'count'])
    xf = xf.sort('count', ascending = False)
    xf['year'] = year
    df = df.append(xf, ignore_index = True)
    # add to set of top names by sex
    for sex, nameset in topnames.items():
        _nx = xf[xf.sex == sex]
        nameset.update(_nx[0:50]['name'])
        # then get counts by year
        yearcounts = yearcounts.append({'sex': sex, 'year': year,
            'total': sum(_nx['count']), 'top50': sum(_nx['count'][0:50])}, ignore_index = True)




# now that we have every name
# get top 50 names per sex per year
# write csvs
arr = []
for sex, names in topnames.items():
    ycounts = yearcounts[yearcounts.sex == sex].set_index('year')
    for name in list(names):
        ndf = df[(df.sex == sex) & (df.name == name)].set_index('year')
        ndf['per_100k'] = pd.Series.round(ndf['count'] * 100000 /  ycounts['total'])
        ndf['pct_change'] = pd.Series.round(ndf['per_100k'].pct_change() * 100, 1)

        npath = os.path.join(NAMES_FILES_DIR, sex, name + '.csv')
        print("Writing", '%s/%s' % (sex, name))
        ndf.drop('name', axis = 1).to_csv(npath, index_label = 'year')
