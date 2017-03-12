from bs4 import BeautifulSoup
from urllib.parse import *
from datetime import *
from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY
import os, sys


def get_html(codemap, pwd):
	text = ""
	for i, code in enumerate(codemap[:30]):
		idx = int(code) +  ord(pwd[i%6])
		ch = chr(idx) if idx > -1 else '.'
		text += ch
	return text


def get_password(file, startDate, endDate):
	if not os.path.exists(file):
		print('the file path {}-> Does not exists!'.format(file))
		return 0
	else:
		with open(file) as fp:
			soup = BeautifulSoup(fp.read(), 'html.parser')
			t = soup.find('input', {'type':'hidden'})['value']
			if not t:
				print('Cannot encrypt this file')
				return 0
	try:
		startDate = parse(startDate)
		endDate = parse(endDate)
	except Exception as e:
		print('Cannot parse date format.')
		print('Please Input date option format like this -s 20140102, -e 2020-11-11...')
		return 0
	else:
		if startDate > endDate:
			print('date range error (startDate must be smaller than endDate)')
			return 0 	
		codemap = unquote(t).split(',')
	
	for date in rrule(DAILY, count=(endDate-startDate).days, dtstart=startDate):
		pwd = date.strftime("%y%m%d")
		soup = BeautifulSoup(get_html(codemap, pwd), 'html.parser')
		if soup.title:
			return pwd
	else:
		print('Find Password Failult!')
		return 0
