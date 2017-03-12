from collections import OrderedDict
from itertools import groupby
from copy import deepcopy
from operator import itemgetter


class RecordParser:
	def __init__(self, records, drop_row_criteria=lambda row:row):
		self.records = [row for row in records if not drop_row_criteria(row)]
		self.fieldSet = list(records[0])

	def __getitem__(self, index):
		if self.records:
			return self.records[index]

	def __len__(self):
		return len(self.records)

	def select(self, fields=[], where=lambda row:row):
		if fields == []:
			columns = self.records[0].keys()
		else:
			columns = [fld for fld in fields if fld in self.fieldSet]
		self.records = [OrderedDict((k, row[k]) for k in columns if k in row) for row in self.records if where(row)]
		self.fieldSet = columns
		return self

	def add_column(self, columns=[]):
		for record in self.records:
			for colname, value in columns:
				record[colname] = value
		for column in columns:
			self.fieldSet.append(column[0])
		return self

	def drop_column(self, columns=[]):
		for record in self.records:
			for column in columns:
				record.pop(column)
		for column in columns:
			self.fieldSet.remove(column)
		return self

	def update(self, bootstrap=[], where=lambda row:row):
		for row in self.records:
			if not where(row):
				continue
			for column, func in bootstrap:
				row[column] = func(row)
		return self

	def order_by(self, *rules):
		for rule in reversed(rules):
			rvs = rule.startswith('-')
			rule = rule.strip('-')
			self.records.sort(key=lambda x: x[rule], reverse=rvs)
		return self

	def group_by(self, annotations, selects=[], dummy=[]): # annotations =  {tgt_col:[('new_col1', 'ano_col1','ano_func1'), ('new_col2', 'ano_col2', 'ano_func2')]}
		ret = []
		cols = []
		records = deepcopy(self.records)
		for column, anno_funcs in annotations.items():
			cols =[column] + [e[0] for e in anno_funcs]
			for g, l in groupby(sorted(records, key=itemgetter(column)), key=itemgetter(column)):
				queryset = list(l)
				new_row = queryset[0] 
				new_row[column] = queryset[0][column]
				for new_col, ano_col, func in anno_funcs:
					val = func([row[ano_col] for row in queryset])
					new_row[new_col] = val
				ret.append(new_row)
		return [OrderedDict((k, '' if k in dummy else row[k]) for k in selects or cols) for row in ret]

