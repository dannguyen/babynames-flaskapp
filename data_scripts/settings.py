import os
import re
import csv

from glob import glob
DATA_SCRIPTS_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(DATA_SCRIPTS_DIR, '../data-hold')
DOWNLOADED_DIR = os.path.join(DATA_DIR, "downloaded")
NAMES_FILES_DIR = os.path.join(DATA_DIR, "names")
# explanation for earliest year at 1950
# http://www.prooffreader.com/2014/07/graphing-problematic-aspects-of-us-baby.html
EARLIEST_YEAR = 1950

for d in [DOWNLOADED_DIR, NAMES_FILES_DIR + '/M', NAMES_FILES_DIR + '/F']:
    os.makedirs(d, exist_ok = True)


def downloaded_fnames():
    return sorted(glob(os.path.join(DOWNLOADED_DIR, '*.txt')))

def downloaded_and_valid_fnames(yr = EARLIEST_YEAR):
    return [f for f in downloaded_fnames() if extract_year_from_fname(f) >= yr]

def extract_year_from_fname(fname):
    return int(re.search('\d{4}', os.path.basename(fname)).group())


def load_data_by_sex_and_name(sex, name):
    fname = os.path.join(NAMES_FILES_DIR, sex, name + '.csv')
    # with open(fname) as f:
    #     data = csv.DictReader(f)
    f = open(fname)
    data = csv.DictReader(f)
    return list(data)


def get_all_names_by_sex():
    """
    returns a alphabetized dict
    {'M': ['David', 'Bob'], 'F': ['Sarah', 'Lisa'] }
    """
    d = {}
    for sex in ['M', 'F']:
        nfiles = glob(os.path.join(NAMES_FILES_DIR, sex, '*.csv'))
        d[sex] = [os.path.basename(n).split('.csv')[0] for n in nfiles]

    return d







import matplotlib.pyplot as plt
import urllib.parse
import base64
from io import BytesIO

def make_image_uri(xarr, yarr):
    fig, axarr = plt.subplots()
    axarr.plot(xarr, yarr)
    # fig = plt.gcf()

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)  # rewind the data
    plt.close(fig)
    uri = 'data:image/png;base64,' + base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return uri

# base64.b64decode(b).decode('utf-8')
