import requests
import os
import datetime
from dateutil.parser import parse as parsedate

def is_modified(url, dstFile):
    r = requests.head(url)
    url_time = r.headers['last-modified']
    url_date = parsedate(url_time)
    file_time = datetime.datetime.fromtimestamp(os.path.getmtime(dstFile))
    print(url_date.timestamp(), file_time.timestamp())
    return url_date.timestamp() > file_time.timestamp()

print(is_modified('https://stackoverflow.com/questions/29314287/python-requests-download-only-if-newer', b'C:\Users\Dor\Desktop\web\index\index.html'))
