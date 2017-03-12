from urllib.request import urlopen
from json import load
import re
import requests


r = requests.get('http://jsonip.com').json()['ip']

print(r)
