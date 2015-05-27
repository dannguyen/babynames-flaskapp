from io import BytesIO
from zipfile import ZipFile
from settings import DOWNLOADED_DIR
import requests

ZIPURL = 'http://www.ssa.gov/OACT/babynames/names.zip'
print("Downloading:", ZIPURL)
with ZipFile(BytesIO(requests.get(ZIPURL).content)) as zfile:
    zfile.extractall(DOWNLOADED_DIR)
